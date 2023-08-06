#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# basic functions for lines

import sys, os
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.color import color as color


__all__ = ['line']

# List of all available line properties, including Style and Width
LineStyleList = ['Solid', 'Dashed', 'Dashdot', 'Dotted', 'None']
LineWidthList = [i for i in range(1, 20)]


class line:
    # Pack all functions as a class
    #
    LineStyleList = LineStyleList
    LineWidthList = LineWidthList
    LineColorList = color.ColorList