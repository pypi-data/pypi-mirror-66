#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# horizon processing functions

from PyQt5 import QtCore
import sys, os
import numpy as np
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])


__all__ = ['analysis']


def checkHorizon(horizon):
    """
    Check if a horizon dictionary in the correct format

    Args:
        horizon:  Horizon as a dictionary with at least the following keys: 'HorizonInfo', 'HorizonData', and 'Z'

    Return:
        True or false
    """

    if type(horizon) is not dict or len(horizon.keys()) < 1:
        return False
    #
    if 'HorizonInfo' not in horizon.keys() or 'HorizonData' not in horizon.keys():
            return False
    if type(horizon['HorizonInfo']) is not dict or len(horizon['HorizonInfo'].keys()) < 1:
        return False
    if 'ILStart' not in horizon['HorizonInfo'].keys():
        return False
    if 'ILEnd' not in horizon['HorizonInfo'].keys():
        return False
    if 'ILStep' not in horizon['HorizonInfo'].keys():
        return False
    if 'ILNum' not in horizon['HorizonInfo'].keys():
        return False
    if 'ILRange' not in horizon['HorizonInfo'].keys():
        return False
    if 'XLStart' not in horizon['HorizonInfo'].keys():
        return False
    if 'XLEnd' not in horizon['HorizonInfo'].keys():
        return False
    if 'XLStep' not in horizon['HorizonInfo'].keys():
        return False
    if 'XLNum' not in horizon['HorizonInfo'].keys():
        return False
    if 'XLRange' not in horizon['HorizonInfo'].keys():
        return False
    if type(horizon['HorizonData']) is not dict or len(horizon['HorizonData'].keys()) < 1:
        return False
    if 'Z' not in horizon['HorizonData'].keys():
        return False
    #
    return True


def convertHorizon2PointSet(horizon, undefined_value=np.NaN, property_list=[]):
    """
    Convert a horizon dictionary to pointset dictionary
    Args:
        horizon:    Horizon as a dictionary
    Return:
         pointset dictionary
    """
    _pointset = {}
    if checkHorizon(horizon) is False:
        return _pointset
    #
    _inl = horizon['HorizonInfo']['ILRange']
    _xl = horizon['HorizonInfo']['XLRange']
    _z = horizon['HorizonData']['Z']
    #
    _z = np.reshape(_z, [-1])
    #
    _idx = np.linspace(0, len(_inl) * len(_xl) - 1, len(_inl) * len(_xl)).astype(int)
    if np.isnan(undefined_value):
        _idx = _idx[~np.isnan(_z)]
    else:
        _idx = _idx[~(_z==undefined_value)]
    #
    _pointset['Inline'] = _inl[(_idx / len(_xl)).astype(int)]
    _pointset['Crossline'] = _xl[(_idx % len(_xl)).astype(int)]
    _pointset['Z'] = _z[_idx]
    #
    for _f in property_list:
        if _f in horizon['HorizonData'].keys() and _f != 'Z':
            _pointset[_f] = np.reshape(horizon['HorizonData'][_f], [-1])[_idx]
    #
    # reshape
    for _f in _pointset.keys():
        _pointset[_f] = np.reshape(_pointset[_f], [-1, 1])
    #
    return _pointset


def convertPointSet2Horizon(pointset, property_list=[], filling_up_value=np.NaN):
    from cognitivegeo.src.pointset.analysis import analysis as pointset_ays
    return pointset_ays.convertPointSet2Horizon(pointset=pointset,
                                                property_list=property_list,
                                                filling_up_value=filling_up_value)


class analysis:
    checkHorizon = checkHorizon
    #
    convertHorizon2PointSet = convertHorizon2PointSet
    convertPointSet2Horizon = convertPointSet2Horizon