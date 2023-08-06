#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

from __future__ import absolute_import, division, print_function

__version__ = '1.0'

__all__ = ['basic', 'core', 'vis', 'seismic', 'psseismic', 'horizon', 'pointset', 'gui',
           'start']

import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-6])

import gaeio.src.basic as basic
import gaeio.src.core as core
import gaeio.src.vis as vis
import gaeio.src.seismic as seismic
import gaeio.src.psseismic as psseismic
import gaeio.src.horizon as horizon
import gaeio.src.pointset as pointset
import gaeio.src.gui as gui

def start(path=os.path.dirname(__file__)):
    """
    Start the GUI
    Args:
        path: starting path. Default is the package.
    Return:
        N/A
    """
    gui.start(startpath=path)

if __name__ == "__main__":
    start()