# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['convert', 'utaromkan']
setup_kwargs = {
    'name': 'utaromkan',
    'version': '1.4.0',
    'description': 'kana <-> romaji conversion for utau',
    'long_description': "utaromkan\n-----------\n\nutaromkan is a module that does very simple and limited conversion between\nhiragana and romaji in the most conventionally excepted way in the utau community.\n\nIt's forked from uromkan, which you can find here https://github.com/jmoiron/uromkan/\n\ninstall\n---------\n`pip install utaromkan`\n\ncommands\n---------\nyou can launch utaromkan.py to use the gui, or you can use the commands within a script to convert\n\n`romgan(str)`\n\nconverts romaji string -> hiragana string\n\n`ganrom(str)`\n\nconverts hiragana string -> romaji string\n",
    'author': 'Tart',
    'author_email': 'conemusicproductions@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/danalog/utaromkan/',
    'py_modules': modules,
}


setup(**setup_kwargs)
