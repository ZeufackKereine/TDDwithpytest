from setuptools import setup, find_packages

setup(
    name="flaskner",  # Name of your package
    version="0.0.1",  # Initial version of the package
    description="A simple Named Entity Recognition (NER) API using Flask",  # Description
    packages=find_packages(),  # Automatically find packages in the project
    install_requires=[
        "Flask>=2.0.0",  # Flask as a dependency
        "spacy>=3.0.0",  # spaCy for NER functionality
    ],
)