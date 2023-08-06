#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

from __future__ import absolute_import, division, print_function

__all__ = ['keyboard', 'settings']


import os, sys
sys.path.append(os.path.dirname(__file__)[:-5][:-4][:-6])
#
from gaeio.src.core.keyboard import keyboard as keyboard
from gaeio.src.core.settings import settings as settings