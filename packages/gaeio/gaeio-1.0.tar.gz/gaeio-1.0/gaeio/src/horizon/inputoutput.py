#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# horizon data IO

import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.messager import messager as vis_msg
from gaeio.src.pointset.inputoutput import inputoutput as pointset_io
from gaeio.src.horizon.analysis import  analysis as horizon_ays


__all__ = ['inputoutput']

def readHorizonFromAscii(asciifile, comment='#', delimiter=None,
                         inlcol=0, xlcol=1, zcol=2, filling_up_value=np.NaN, undefined_value=-999):
    """
    Read horizon from an ASCII file (by numpy.loadtxt)

    Args:
        asciifile:          An ASCII file for reading
        comment:            Comments. Default is '#'
        delimiter:          Delimiter. Default is None
        inlcol:             Index of the inline column. Default is 0
        xlcol:              Index of the crossline column. Default is 1
        zcol:               Index of the z column. Default is 2
        filling_up_value:   value to fill up non-existing locations. Default is NaN
        undefined_value:    values to skip as undefined. Default is -999
    Return:
        2D array of the horizon from the ASCII file, with inline at column 0, crossline at column 1, and z at column 2
    """

    if os.path.exists(asciifile) is False:
        vis_msg.print("ERROR in readPointFromAscii: Pointset file not found", type='error')
        sys.exit()
    # read pointset
    _pointset = pointset_io.readPointSetFromAscii(asciifile=asciifile, comment=comment, delimiter=delimiter,
                                                  inlcol=inlcol, xlcol=xlcol, zcol=zcol,
                                                  undefined_value=undefined_value)
    # convert pointset to horizon
    _horizon = horizon_ays.convertPointSet2Horizon(_pointset, filling_up_value=filling_up_value,
                                                   property_list=list(_pointset.keys()))
    #
    return _horizon


def writeHorizonToAscii(horizon, asciifile, property_list=[]):
    """
    Write pointset to ascii file
    Args:
        horizon:        horizon dictionary
        ascillfile:     file name
        property_list:  List of properties
    Return:
        N/A
    """
    if horizon_ays.checkHorizon(horizon) is False:
        print('ERROR in writeHorizonToAscii: Horizon dictionary expected')
        sys.exit()
    #
    # convert horizon to pointset
    _pointset = horizon_ays.convertHorizon2PointSet(horizon=horizon, property_list=property_list)
    #
    # write to ascii
    pointset_io.writePointSetToAscii(pointset=_pointset, asciifile=asciifile)


class inputoutput:
    # group all functions as a single class
    readHorizonFromAscii = readHorizonFromAscii
    writeHorizonToAscii = writeHorizonToAscii