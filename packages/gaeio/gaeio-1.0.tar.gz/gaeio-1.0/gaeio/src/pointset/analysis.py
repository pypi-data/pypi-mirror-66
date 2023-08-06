#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# pointset processing functions

from PyQt5 import QtCore
import sys, os
import numpy as np
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])

__all__ = ['analysis']


def checkPointSet(point):
    """
    Check if a pointset dictionary in the correct format

    Args:
        point:  Points as a dictionary with at least the following keys: 'Inline', 'Crossline', and 'Z'

    Return:
        True or false
    """

    if type(point) is not dict or len(point.keys()) < 1:
        return False
    #
    if 'Inline' not in point.keys() or 'Crossline' not in point.keys() or 'Z' not in point.keys():
            return False
    #
    return True


def checkPointSet_Multiple(pointset, p_list=[]):
    """
    Check if multiple pointset dictionaries in the correct format

    Args:
        point:  Pointsets as a dictionary with each key representing a point dictionary.
                Each point dictionary contains at least the following keys: 'Inline', 'Crossline', and 'Z'

    Return:
        True or false
    """

    if type(pointset) is not dict or len(pointset.keys()) < 1:
        return False
    if p_list is None or len(p_list) < 1:
        return False
    for p in p_list:
        if pointset[p] is None:
            return False
        if checkPointSet(pointset[p]) is False:
            return False
    return True


def convertPointSet2Horizon(pointset, property_list=[], filling_up_value=np.NaN):
    """
    Convert a pointset dictionary to horizon dictionary
    Args:
        pointset:           PointSet as a dictionary
        property_list:      list of property for conversion
        filling_up_value:   values to fill up
    Return:
         horizon dictionary
    """
    _horizon = {}
    if checkPointSet(pointset) is False:
        return _horizon
    #
    # get inline and xline info
    _inl = np.unique(pointset['Inline'])
    _xl = np.unique(pointset['Crossline'])
    _inlstart = np.min(_inl)
    _inlend = np.max(_inl)
    _xlstart = np.min(_xl)
    _xlend = np.max(_xl)
    _inlstep = 1
    _xlstep = 1
    if len(_inl) > 1:
        _inlstep = np.min(_inl[1:] - _inl[0:-1])
    if len(_xl) > 1:
        _xlstep = np.min(_xl[1:] - _xl[0:-1])
    _inlnum = (_inlend - _inlstart) / _inlstep + 1
    _inlnum = np.round(_inlnum).astype(np.int32)
    _xlnum = (_xlend - _xlstart) / _xlstep + 1
    _xlnum = np.round(_xlnum).astype(np.int32)
    _inlend = _inlstart + (_inlnum - 1) * _inlstep
    _xlend = _xlstart + (_xlnum - 1) * _xlstep
    _inlrange = np.linspace(_inlstart, _inlend, _inlnum)
    _xlrange = np.linspace(_xlstart, _xlend, _xlnum)
    #
    _horizon['HorizonInfo'] = {}
    _horizon['HorizonInfo']['ILStart'] = _inlstart
    _horizon['HorizonInfo']['ILEnd'] = _inlend
    _horizon['HorizonInfo']['ILStep'] = _inlstep
    _horizon['HorizonInfo']['ILNum'] = _inlnum
    _horizon['HorizonInfo']['ILRange'] = _inlrange
    _horizon['HorizonInfo']['XLStart'] = _xlstart
    _horizon['HorizonInfo']['XLEnd'] = _xlend
    _horizon['HorizonInfo']['XLStep'] = _xlstep
    _horizon['HorizonInfo']['XLNum'] = _xlnum
    _horizon['HorizonInfo']['XLRange'] = _xlrange
    #
    _hrzdata = {}
    _hrzdata['Z'] = np.ones([_inlnum, _xlnum]) * filling_up_value
    for _i in range(np.shape(pointset['Z'])[0]):
        _inlidx = int((pointset['Inline'][_i, 0] - _inlstart) / _inlstep)
        _xlidx = int((pointset['Crossline'][_i, 0] - _xlstart) / _xlstep)
        #
        if _inlidx >= 0 and _inlidx < _inlnum and _xlidx >= 0 and _xlidx < _xlnum:
            _hrzdata['Z'][_inlidx, _xlidx] = pointset['Z'][_i, 0]
    # more properties
    for _p in property_list:
        if _p in pointset.keys() and _p != 'Z' and _p != 'Inline' and _p != 'Crossline':
            _hrzdata[_p] = np.ones([_inlnum, _xlnum]) * filling_up_value
            #
            for _i in range(np.shape(pointset[_p])[0]):
                _inlidx = int((pointset['Inline'][_i, 0] - _inlstart) / _inlstep)
                _xlidx = int((pointset['Crossline'][_i, 0] - _xlstart) / _xlstep)
                #
                if _inlidx >= 0 and _inlidx < _inlnum and _xlidx >= 0 and _xlidx < _xlnum:
                    _hrzdata[_p][_inlidx, _xlidx] = pointset[_p][_i, 0]
    #
    _horizon['HorizonData'] = _hrzdata
    #
    return _horizon


def convertHorizon2PointSet(horizon, undefined_value=np.NaN, property_list=[]):
    from cognitivegeo.src.horizon.analysis import analysis as horizon_ays
    return horizon_ays.convertHorizon2PointSet(horizon=horizon, undefined_value=undefined_value,
                                               property_list=property_list)


class analysis:
    checkPointSet = checkPointSet
    checkPointSet_Multiple = checkPointSet_Multiple
    #
    convertPointSet2Horizon = convertPointSet2Horizon
    convertHorizon2PointSet = convertHorizon2PointSet