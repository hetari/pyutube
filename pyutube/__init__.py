"""This is the initialization module for the pyutube package.

It provides the main entry point for the package by importing the `app`
object from the `cli` submodule.

Example:
    To use this package, you can import the `app` object directly:

    >>> from pyutube import app
    >>> app.run()

"""
from .cli import app as app


# List the symbols you want to export from this module
# __all__ = ['app']
