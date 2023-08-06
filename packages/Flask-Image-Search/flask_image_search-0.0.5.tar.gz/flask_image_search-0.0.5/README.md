## Installation

Run the following to install
```commandline
pip install flask_image_search
```
Run the following to install from github
```commandline
pip install git+https://github.com/hananf11/flask_image_search.git
```

## Usage
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_image_search import ImageSearch

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)

image_search = ImageSearch(app, db)


@image_search.register(fk_cols=['model_id'])  # register the image model_ and track the also track the model_id column
class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    model_id = db.Column(db.ForeignKey('models.id'))

    model = db.relationship('Model', primaryjoin='Image.model_id == Model.id', backref="images")


image_search.index_model(Image)


class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)


images = Image.query.with_transformation(image_search.query_search(image_path='query.jpg', limit=5)).all()
print(images)
models = Model.query.with_transformation(image_search.query_relation_search(image_path='query.jpg', limit=5)).all()
print(models)
```