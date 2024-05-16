import logging
from logging import NullHandler

logging.getLogger("cascade").addHandler(NullHandler())

__author__ = "Seth Girvin"
__email__ = "sgirvin@compass.ie"
__version__ = "2.1.0"
