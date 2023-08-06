import logging
import os
import shutil
import threading
import time
from difflib import get_close_matches
from logging import getLogger, StreamHandler, Formatter
from types import SimpleNamespace
from zipfile import BadZipFile

import numpy as np
from PIL import Image
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.expression import case
from sqlalchemy import event

Image.LOAD_TRUNCATED_IMAGES = True  # this stops truncated image errors on large image files

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
handler = StreamHandler()
formatter = Formatter('%(asctime)s flask image search: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class MultiFileSaver(object):
    """
    This class is used as a cool down for saving the new image data
    It also backs up the most recent version of indexed data before save so that if the program is terminated it dose not leave a corrupted file
    """

    def __init__(self):
        self.save_data = {}
        self.wait_time = 2
        self.threading_timer = None
        self.time_timer = None

    def save(self):
        # fist clear all the timers
        if self.threading_timer is not None:
            self.threading_timer.cancel()

        start = time.time()
        for file, data in self.save_data.items():
            # file = os.path.join(os.getcwd(), file)
            if not os.path.exists(os.path.split(file)[0]):
                os.mkdir(os.path.split(file)[0])
            if os.path.exists(file):
                shutil.copyfile(file, file + 'bak')
            np.savez_compressed(file, **data)
        total_time = time.time() - start
        self.wait_time = total_time + .5

    def saver(self, file_path):
        """this function returns inner saver that can be called to update the save data"""

        def inner_saver(new_data):
            self.save_data[file_path] = new_data
            if self.threading_timer is not None:  # check there is a timer set
                self.threading_timer.cancel()

            if self.time_timer is None:  # check if there is a timer set
                self.time_timer = time.time()  # start the timer because this is the fist call since last save/start
            elif time.time() - self.time_timer >= 60 + self.wait_time:
                # this should run about every minuet since the file save was called unless it was saved before then
                # adding the wait_time means that if the save takes longer that 1 min it wont cause any errors
                self.time_timer = None
                self.threading_timer = None
                self.save()  # save the file now
                return None  # exit because the file was saved

            self.threading_timer = threading.Timer(self.wait_time, self.save)
            self.threading_timer.start()

        return inner_saver


class ImageSearch(object):
    def __init__(self, app, db, no_tf=None):
        self.app = app
        self.models = {}
        self.indexed_models = []
        if app is not None:
            self.app_init(app, db, no_tf)

    def app_init(self, app, db, no_tf=None):
        if no_tf is None:
            if app.debug:
                """tensorflow has errors running in debug with reload"""
                logger.warning(
                    "tensorflow has not been loaded meaning images will not be indexed or searched correctly")
                logger.warning("set no_tf to false to load in tensorflow or disable debug")
                no_tf = True
        self.db = db

        self.is_running = threading.Event()
        self.is_registering = threading.Event()
        self.app_path = os.path.dirname(app.instance_path)  # get the path to the flask app

        self.safe_save = MultiFileSaver()  # safe saver for writing to the index files

        self.file_prefix = app.config.get("IMAGE_SEARCH_FILE_PATH_PREFIX", 'image_search_features/')

        def background_setup():
            """this function runs in a thread so it is no blocking"""
            if no_tf:
                from .feature_extractor_debug import FeatureExtractor
            else:
                from .feature_extractor import FeatureExtractor

            self.feature_extractor = FeatureExtractor()
            self.is_running.set()

        thread = threading.Thread(target=background_setup)  # run this in the background
        thread.start()

    def register(self, url_column='url', id_col=None, fk_cols=None):
        """
        decorator for registering models to be indexed
        :param url_column: the column where the url is located
        :param id_col: the name of the id column to be used
        :param fk_cols: list of the names foreign keys to be tracked
        :return:
        """
        if fk_cols is None:
            fk_cols = []

        # clear the registering flag so that function needing a registered model_ know to wait
        self.is_registering.clear()

        def decorator_inner(model):
            def thread_content():  # run this in a thread
                # wait till setup has finished
                self.is_running.wait()

                self.indexed_models.append(model.__tablename__)

                # work out the path for the index file
                feature_file = os.path.join(os.getcwd(), self.file_prefix + model.__tablename__ + '.npz')

                # save the data using the tablename as the identifier
                self.models[model.__tablename__] = SimpleNamespace(
                    data={},  # this stores image features
                    url_column=url_column,
                    saver=self.safe_save.saver(feature_file),  # create safe_save saver for saving to the file
                    id_column=id_col or inspect(model).primary_key[0].name,
                    fk_columns=fk_cols
                )

                data = self.models[model.__tablename__]  # crate variable that points to the data in self.models

                @event.listens_for(model, "after_delete")
                def deleted_model(mapper, connection, target):
                    self.delete_index(target)

                @event.listens_for(model, "after_insert")
                def inserted_model(mapper, connection, target):
                    self.index(target)

                @event.listens_for(model, "after_update")
                def updated_model(mapper, connection, target):
                    self.index(target, override=True)

                count = 0
                # load the indexed data
                if os.path.exists(feature_file) or os.path.exists(feature_file + 'bak'):
                    # load in the data or the backup of data if it corrupt
                    try:
                        with np.load(feature_file) as file:
                            for index in file.files:
                                count += 1
                                data.data[index] = file[index]
                    except (ValueError, IOError, BadZipFile, AttributeError):
                        try:
                            with np.load(feature_file + 'bak') as file:
                                # replace the corrupt file with the backup
                                shutil.copy(feature_file + 'bak', feature_file)

                                for index in file.files:
                                    count += 1
                                    data.data[index] = file[index]
                        except (ValueError, IOError, BadZipFile, AttributeError):
                            logger.error("failed to load data")  # log an error
                logger.info("Loaded in {} images for the model '{}'".format(count, model.__tablename__))
                # todo: remove this sleep and fix the error
                time.sleep(2)  # this wait stops server error being thrown if a search is happening
                self.is_registering.set()

            thread = threading.Thread(target=thread_content)
            thread.start()

            return model

        return decorator_inner

    def index(self, entry, override=False):
        """this is for indexing one image"""
        self.is_running.wait()
        self.is_registering.wait()

        data = self.models[entry.__tablename__]

        image_id = "_".join(
            [str(getattr(entry, id_column)) for id_column in [data.id_column] + data.fk_columns])

        image_path = getattr(entry, data.url_column)

        if not override and image_id in data.data:
            return False
        image = Image.open(os.path.join(self.app_path, image_path.strip('/')))
        image_features = self.feature_extractor.extract(image)  # extract the features from the image
        data.data[image_id] = image_features  # save the image feature in data
        data.saver(data.data)  # save the file
        return True

    def index_model(self, model, override=False):
        """index entire model"""

        def thread_content():  # run the function in the backgound
            self.is_registering.wait()
            self.is_running.wait()

            start_time = time.time()

            data = self.models[model.__tablename__]

            entries = self.db.session.query(model).all()

            successful = 0

            for entry in entries:
                # construct string that is used as the file name

                success = self.index(entry, override)  # finally index the image
                if success:
                    successful += 1

            if successful != 0:
                logger.info(f"successfully indexed {successful} new images in {time.time() - start_time}s")
            else:
                logger.info(f"no new images were indexed")

        thread = threading.Thread(target=thread_content)
        thread.start()

    def delete_index(self, model):
        """delete an index"""
        data = self.models[model.__tablename__]
        # work out the feature id of the indexed data
        feature_id = "_".join([str(getattr(model, id_column)) for id_column in [data.id_column] + data.fk_columns])
        # try and delete the index data
        try:
            del data.data[feature_id]
            data.saver(data.data)
        except KeyError:
            pass

    def search(self, model_name, image_path=None, image_data=None, limit=-1):
        self.is_running.wait()  # wait till the app is running
        self.is_registering.wait()  # wait till the app is not registering a model_
        if image_path is not None:  # if the image path is being used set image_data to the opened image
            image_data = Image.open(os.path.join(os.getcwd(), image_path))

        image_features = self.feature_extractor.extract(image_data)  # get the image features

        feature_ids, features = zip(*self.models[model_name].data.items())  # split the feature_ids and feature

        distances = np.linalg.norm(features - image_features, axis=1)  # compare the search image with all other images
        distances_sorted = np.argsort(distances)  # order the items by distance

        if limit != -1:  # trim the sorted data if limit is set
            distances_sorted = distances_sorted[:limit]

        # return a list of feature ids and distances
        return [(feature_ids[uid], distances[uid]) for uid in distances_sorted]

    def query_search(self, model=None, image_path=None, image_data=None, limit=20):
        def inner(query):
            if image_data is None and image_path is None:
                return query
            self.is_running.wait()
            self.is_registering.wait()

            column_descriptions = query.column_descriptions
            if model is None:
                if len(column_descriptions) > 1:
                    raise Exception("Please specify the model, could not work out model")
                else:
                    model_ = column_descriptions[0]["type"]
            else:
                model_ = model

            data = self.models[model_.__tablename__]

            results = self.search(model_.__tablename__, image_path, image_data, limit)  # get the search

            # apply search results to query
            model_id_column = getattr(model_, data.id_column)  # get the id column object
            # construct case statement for applying the weights
            feature_ids = []
            case_list = []
            for feature_id, weight in results:
                feature_ids.append(feature_id.split("_")[0])
                case_list.append((model_id_column == feature_id.split("_")[0], float(weight)))
            case_statement = case(case_list, else_=None).label("weight")
            return query.order_by(case_statement).filter(model_id_column.in_(feature_ids))

        return inner

    def query_relation_search(self, model=None, model_id_column=None, relation_column=None, foreign_key_column=None,
                              image_path=None,
                              image_data=None, limit=20):
        # todo: make this call query search to cut down on duplicate code
        if image_path is not None or image_data is not None:
            def inner(query):
                self.is_running.wait()
                self.is_registering.wait()

                column_descriptions = query.column_descriptions
                if model is None:
                    if len(column_descriptions) > 1:
                        raise Exception("Please specify the model, could not work out model")
                    else:
                        model_ = column_descriptions[0]["type"]
                else:
                    model_ = model

                # work out the related column
                if relation_column is None:
                    for value in inspect(model_).relationships.values():
                        value_model = value.mapper.class_
                        if value_model.__tablename__ in self.indexed_models:
                            relation_column_ = value.class_attribute
                            break
                    else:
                        raise Exception("No valid relation column could be found. ")
                else:
                    relation_column_ = relation_column

                related_model = relation_column_.property.mapper.class_

                data = self.models[related_model.__tablename__]

                # work out the foreign key column
                if foreign_key_column is None:
                    for foreign_key_col in relation_column_.property.remote_side:
                        if foreign_key_col.name in data.fk_columns:
                            fk_column = foreign_key_col
                            break
                    else:
                        raise Exception("No foreign key could be found.")
                else:
                    fk_column = foreign_key_column

                # get the model id column
                if model_id_column is None:
                    for fk in fk_column.foreign_keys:
                        if fk.column.primary_key:
                            model_id_column_ = fk.column
                            break
                    else:
                        raise Exception("could not find a valid model id column.")
                else:
                    model_id_column_ = model_id_column

                # get the index because this is used to retrieve the value from the feature_id
                fk_value_index = data.fk_columns.index(fk_column.name)

                related_model_id_column = getattr(related_model, data.id_column)

                related_model_ids = []
                model_ids = []
                feature_weights = []

                results = self.search(related_model.__tablename__, image_path, image_data)
                for uid, weight in results:
                    related_model_id, *fk_values = map(int, uid.split('_'))
                    fk_value = fk_values[fk_value_index]
                    if len(model_ids) < limit or fk_value in model_ids:
                        related_model_ids.append(int(related_model_id))
                        feature_weights.append(float(weight))
                        if fk_value not in model_ids:
                            model_ids.append(int(fk_value))

                case_statement = self.db.case([(related_model_id_column == uid, weight) for uid, weight in
                                               zip(related_model_ids, feature_weights)], else_=None).label("weight")
                new_q = query.join(related_model).options(self.db.contains_eager(relation_column_)).filter(
                    model_id_column_.in_(model_ids)).order_by(case_statement)

                return new_q

            return inner
        else:
            return lambda q: q  # because there is no image just return the query
