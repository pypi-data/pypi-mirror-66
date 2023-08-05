# in this file, we must first install the DB
# load the words in the DB
# then the user can simply import the lib and start
# using it


#!/usr/bin/env python
# -*- coding: utf8 -*-
import os


from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".txt"):
                paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('wordstats/language_data/')

setup(
    name="wordstats",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="Mircea Lungu",
    author_email="me@mir.lu",
    description="Word frequency stats for your python fingertips ",
    keywords="second language acquisition api",
    package_data={'': extra_files},
    install_requires=("configobj",
                      "sqlalchemy")
)
