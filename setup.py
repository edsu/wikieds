from setuptools import setup

description = 'Command line tool to Print a markdown summary of editors for a Wikipedia article.'

setup(
    name = 'wikieds',
    version = '0.0.1',
    url = 'http://github.com/edsu/wikieds',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['wikieds',],
    scripts = ['wikieds.py'],
    description = description
)
