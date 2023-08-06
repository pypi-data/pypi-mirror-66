# -*- coding: utf-8 -*-
"""Provide functionality common to all classes in the package. Very
little is expected to be here, only methods which are clearly common
to all such as default implementations of __str__ and fill-in comparison
functions to ensure total ordering.
"""
from __future__ import unicode_literals

import sys
import logging
import tempfile

from winsys import utils

class _WinSysObject(object):

    def as_string(self):
        """Produce a readable version of the data, used by
        __str__.
        """
        return getattr(self, "name", self.__class__.__name__)

    def __str__(self):
        return self.as_string()

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.as_string())

    def __hash__(self):
        return hash(self.as_string())

    #
    # Each object should provide a useful override for the
    # dumped function, possibly recursing into its own
    # internal items, call their dumped functions at the
    # next level down.
    #
    def dumped(self, level=0):
        return utils.dumped(self.as_string(), level)

    def dump(self, level=0):
        sys.stdout.write(self.dumped(level) + "\n")

    #
    # Fill-in functions to ensure that a complete
    # sortability is maintained. These may be
    # overridden by subclasses (but are not
    # expected to be).
    #
    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return not (self == other) and not (self < other)

    def __ge__(self, other):
        return self > other or self == other

    def __le__(self, other):
        return self < other or self == other

class Unset(object):
    def __repr__(self):
        return "<Unset>"
    def __str__(self):
        return "<Unset>"
    def __nonzero__(self):
        return False
    __bool__ = __nonzero__

UNSET = Unset()

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

#
# Create a logger without any handlers.
#
_logger = logging.getLogger("winsys")
_logger.addHandler(NullHandler())
#~ _logger.addHandler(logging.StreamHandler())
#~ _logger.setLevel(logging.DEBUG)

debug = _logger.debug
log = _logger.log
info = _logger.info
warn = _logger.warn
error = _logger.error
exception = _logger.exception

def add_logging_handler(handler):
    _logger.addHandler(handler)

def remove_logging_handler(handler):
    _logger.removeHandler(handler)
