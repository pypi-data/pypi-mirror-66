from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flask_image_search',
    version='0.0.5',
    description="Flask Image Search works with Flask-SQLAlchemy to add image searching functionality",
    packages=["flask_image_search"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Topic :: Database"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "Flask>=1.1.1",
        "Flask_SQLAlchemy>=2.4.1",
        "Keras>=2.3.1",
        "numpy>=1.18.1",
        "pillow>=7.1.1",
        "tensorflow>=2.1.0"
    ],
    extra_require={
        "dev": [
            "twine"
        ]
    },
    url="https://github.com/hananf11/flask_image_search",
    author="Hanan Fokkens",
    author_email="hananfokkens@gmail.com"
)
