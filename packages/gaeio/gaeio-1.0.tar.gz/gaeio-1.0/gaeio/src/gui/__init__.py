#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

from __future__ import absolute_import, division, print_function

__version__ = '1.0'


__all__ = ['start']


import os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
#
from gaeio.src.gui.gui_main import start

if __name__ == "__main__":
    start(startpath=os.path.dirname(__file__)[:-8])