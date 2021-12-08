""" lw_pub_statistics

.. module:: lw_pub_statistics
    :synopsis: Describe the project.

.. moduleauthor:: Van Maldeghem Laurian <laurian.van.maldeghem@vliz.be>

"""

from .standardize import *
import logging
from logging import NullHandler

log = logging.getLogger(__name__)
log.addHandler(NullHandler())
