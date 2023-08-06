#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# basic functions for file

import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.messager import messager as vis_msg


__all__ = ['file']


def readAsciiFile(asciifile, comment='#', delimiter=None):
    """
    Read an ASCII file (by numpy.loadtxt)

    Args:
        asciifile:  An ASCII file for reading
        comment:    Comments. Default is '#'
        delimiter:  Delimiter. Default is None

    Return:
        2D array of the data from the ASCII file
    """

    if os.path.exists(asciifile) is False:
        vis_msg.print("ERROR in readAsciiFile: Ascii file not found", type='error')
        sys.exit()
    #
    try:
        return np.loadtxt(asciifile, comments=comment, delimiter=delimiter)
    except ValueError:
        return None


class file:
    # Pack all functions as a class
    readAsciiFile = readAsciiFile
