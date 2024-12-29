import os
from setuptools import setup

setup(
    name="SASL",
    version="1.0",
    description="a compiler for the functional programming language SASL",
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    author="Cato Kurtz and Nico Schreiner",
    packages=["SASL"],
    install_requires=[],
)
