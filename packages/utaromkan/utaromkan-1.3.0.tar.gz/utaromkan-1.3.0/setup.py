# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['convert', 'utaromkan']
setup_kwargs = {
    'name': 'utaromkan',
    'version': '1.3.0',
    'description': 'kana <-> romaji conversion for utau',
    'long_description': "utaromkan\n-----------\n\nutaromkan is a module that does very simple and limited conversion between\nhiragana and romaji in the most conventionally excepted way in the utau community.\n\nIt's forked from uromkan, which you can find here https://github.com/jmoiron/uromkan/\n\n\n",
    'author': 'Tart',
    'author_email': 'conemusicproductions@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/danalog/utaromkan/',
    'py_modules': modules,
}


setup(**setup_kwargs)
