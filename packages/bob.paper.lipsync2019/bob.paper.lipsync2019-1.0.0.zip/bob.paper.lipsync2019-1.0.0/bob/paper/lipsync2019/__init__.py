#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Thu 23 Jun 11:16:22 2016

"""
The methods for the package

"""

from . import script
from . import scripts_db
from . import database
from . import extractor
from . import preprocessor
# from . import playing_around
from . import algorithm

def get_config():
    """
    Returns a string containing the configuration information.

    """
    import bob.extension
    return bob.extension.get_config(__name__)


# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]
