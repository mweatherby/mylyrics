from distutils.core import setup
import setuptools  # noqa
from setuptools import find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='mylyrics',
    version='0.1.0',
    long_description=open('README.md').read(),
    install_requires=requirements,
    url="https://github.com/mweatherby/mylyrics.git",
    packages=find_packages(),
    author="Michael Weatherby",
    author_email="dummy_email@gmail.com",
    )

