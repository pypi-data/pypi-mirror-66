#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# basic functions for markers

import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.color import color as color


__all__ = ['marker']

# List of all available marker properties, including Style and Size
MarkerStyleList = ['*', '+', 'o', 'v', '^', '<', '>',
                   'x', 'X', '.', 'None']
MarkerSizeList = [i for i in range(1, 20)]


class marker:
    # Pack all functions as a class
    #
    MarkerStyleList = MarkerStyleList
    MarkerSizeList = MarkerSizeList
    MarkerColorList = color.ColorList