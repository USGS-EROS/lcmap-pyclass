""" Main bootstrap and configuration module for pyccd.  Any module that
requires configuration or services should import app and obtain the
configuration or service from here.
app.py enables a very basic but sufficient form of loose coupling
by setting names of services & configuration once and allowing other modules
that require these services/information to obtain them by name rather than
directly importing or instantiating.
Module level constructs are only evaluated once in a Python application's
lifecycle, usually at the time of first import. This pattern is borrowed
from Flask.
"""
import os, logging, sys, yaml
from functools import wraps

import numpy as np


############################
# Logging system
############################
# to use the logging from any module:
# import app
# logger = app.logging.getLogger(__name__)
#
# To alter where log messages go or how they are represented,
# configure the
# logging system below.
# iso8601 date format
#__format = '%(asctime)s %(module)s::%(funcName)-20s - %(message)s'
__format = '%(asctime)s.%(msecs)03d %(module)s::%(funcName)-20s - %(message)s'
logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format=__format,
                    datefmt='%Y-%m-%d %H:%M:%S')


# Simplify parameter setting and make it easier for adjustment
class Defaults(dict):
    def __init__(self, config_path='parameters.yaml'):
        with open(config_path, 'r') as f:
            super(Defaults, self).__init__(yaml.load(f.read()))

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError('No such attribute: ' + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError('No such attribute: ' + name)


defaults = Defaults(os.path.join(os.path.dirname(__file__), 'parameters.yaml'))


def ensure_ndarray_input(func):
    """
    Wrapper to ensure inputs to a method are of type ndarray
    This cleans up subsequent code that might need to check for this
    """
    @wraps(func)
    def f(*args, **kwargs):
        return func(*(np.asarray(_) for _ in args), **kwargs)
    return f
