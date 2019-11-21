# coding: utf-8
import setuptools
import graphh

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graphh",
    version=graphh.__version__,
    author="Maëlle Cosson, Pauline Hamon-Giraud, Clément Caillard " +
           "and Romain Tavenard",
    author_email="",
    description="A module to make GraphHopper API queries easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chuuw/graphh/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
