#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# pointset data IO

import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.messager import messager as vis_msg
from gaeio.src.basic.file import file as basic_file
from gaeio.src.basic.matdict import matdict as basic_mdt
from gaeio.src.pointset.analysis import analysis as pointset_ays


__all__ = ['inputoutput']

def readPointSetFromAscii(asciifile, comment='#', delimiter=None,
                       inlcol=0, xlcol=1, zcol=2, undefined_value=-999):
    """
    Read points from an ASCII file (by numpy.loadtxt)

    Args:
        asciifile:          An ASCII file for reading
        comment:            Comments. Default is '#'
        delimiter:          Delimiter. Default is None
        inlcol:             Index of the inline column. Default is 0
        xlcol:              Index of the crossline column. Default is 1
        zcol:               Index of the z column. Default is 2
        undefined_value:    values to skip as undefined. Default is -999
    Return:
        2D array of the points from the ASCII file, with inline at column 0, crossline at column 1, and z at column 2
    """

    if os.path.exists(asciifile) is False:
        vis_msg.print("ERROR in readPointFromAscii: Pointset file not found", type='error')
        sys.exit()
    #
    data = basic_file.readAsciiFile(asciifile=asciifile, comment=comment, delimiter=delimiter)
    #
    npt, ncol = np.shape(data)
    #
    if inlcol >= ncol or inlcol < 0:
        vis_msg.print("ERROR in readPointFromAscii: Inline column index not found", type='error')
        sys.exit()
    if xlcol >= ncol or xlcol < 0:
        vis_msg.print("ERROR in readPointFromAscii: Crossline column index not found", type='error')
        sys.exit()
    if zcol >= ncol or zcol < 0:
        vis_msg.print("ERROR in readPointFromAscii: Z column index not found", type='error')
        sys.exit()
    #
    point = {}
    point['Inline'] = data[:, inlcol:inlcol+1]
    point['Crossline'] = data[:, xlcol:xlcol+1]
    point['Z'] = data[:, zcol:zcol+1]
    # more columns
    idx = 1
    for i in range(ncol):
        if i != inlcol and i != xlcol and i != zcol:
            point['property_'+str(idx)] = data[:, i:i+1]
            idx = idx + 1
    #
    # remove undefined values
    _idx = np.linspace(0, np.shape(point['Z'])[0] - 1, np.shape(point['Z'])[0]).astype(int)
    if np.isnan(undefined_value):
        _idx = _idx[~np.isnan(point['Z'][:, 0])]
    else:
        _idx = _idx[~(point['Z'][:, 0] == undefined_value)]
    for _i in point.keys():
        point[_i] = point[_i][_idx, :]
    #
    return point


def writePointSetToAscii(pointset, asciifile, property_list=[]):
    """
    Write pointset to ascii file
    Args:
        pointset:       pointset dictionary
        ascillfile:     file name
        property_list:  List of properties
    Return:
        N/A
    """
    if pointset_ays.checkPointSet(pointset) is False:
        print('ERROR in writePointSetToAscii: PointSet dictionary expected')
        sys.exit()
    #
    _file = open(asciifile, 'w')
    # write a header
    _file.write("# Headers:\n")
    if 'Inline' in pointset.keys():
        _file.write("# Inline\n")
    if 'Crossline' in pointset.keys():
        _file.write("# Crossline\n")
    if 'Z' in pointset.keys():
        _file.write("# Z\n")
    for j in sorted(property_list):
        if j and pointset.keys() and j != 'Inline' and j != 'Crossline' and j != 'Z':
            _file.write("# " + j + '\n')
    # write points
    _npts = basic_mdt.maxDictConstantRow(pointset)
    for j in range(_npts):
        if 'Inline' in pointset.keys():
            _file.write(str(pointset['Inline'][j, 0]) + '\t')
        if 'Crossline' in pointset.keys():
            _file.write(str(pointset['Crossline'][j, 0]) + '\t')
        if 'Z' in pointset.keys():
            _file.write(str(pointset['Z'][j, 0]) + '\t')
        for k in sorted(property_list):
            if k in pointset.keys() and k != 'Inline' and k != 'Crossline' and k != 'Z':
                _file.write(str(pointset[k][j, 0]) + '\t')
        _file.write('\n')
    #
    _file.close()


class inputoutput:
    # group all functions as a single class
    readPointSetFromAscii = readPointSetFromAscii
    writePointSetToAscii = writePointSetToAscii