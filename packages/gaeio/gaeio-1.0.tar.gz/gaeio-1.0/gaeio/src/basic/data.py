#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# basic functions for processing data

import numpy as np
import os, sys
#
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.messager import messager as vis_msg


__all__ = ['data']


def str2int(str):
    """
    Covert a string to integer

    Args:
        str:    A string for conversion

    Return:
        The corresponding integer if it is convertable. Otherwise, False is returned.
    """

    try:
        return int(str)
    except ValueError:
        if str == 'NAN' or str == 'NaN' or str == 'nan' or str == 'Nan':
            return np.NaN
        else:
            return False


def str2float(str):
    """
    Covert a string to float

    Args:
        str:    A string for conversion

    Return:
        The corresponding float if it is convertable. Otherwise, False is returned.
    """

    try:
        return float(str)
    except ValueError:
        if str == 'NAN' or str == 'NaN' or str == 'nan' or str == 'Nan':
            return np.NaN
        else:
            return False


def not_nan(m):
    """
    Return the not-NaN values in m

    Args:
        m: data

    Return:
         the not-NaN values as a 1D array
    """
    _all_values = np.reshape(m, [-1])
    return _all_values[~np.isnan(_all_values)]


def max(m):
    """
    Return maximum (non-Nan)

    Args:
        m: data

    Return:
         the maximum of all non-NaN values
    """
    return np.max(not_nan(m))

def min(m):
    """
    Return minimum (non-Nan)

    Args:
        m: data

    Return:
        the minimum of all non-NaN values
    """
    return np.min(not_nan(m))


def mean(m):
    """
    Return mean (non-Nan)

    Args:
        m: data

    Return:
        the mean of all non-NaN values
    """
    return np.mean(not_nan(m))


def sum(m):
    """
    Return sum (non-Nan)

    Args:
        m: data

    Return:
        the sum of all non-NaN values
    """
    return np.sum(not_nan(m))


def std(m):
    """
    Return sum (non-Nan)

    Args:
        m: data

    Return:
        the sum of all non-NaN values
    """
    return np.std(not_nan(m))

class data:
    # Pack all functions as a class
    str2int = str2int
    str2float = str2float
    #
    not_nan = not_nan
    max = max
    min = min
    mean = mean
    sum = sum
    std = std
