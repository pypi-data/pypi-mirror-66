#############################################################################################
#                                                                                           #
# Author:   Cognitive Geo                                                                   #
# Email:    cognitivegeo.info@gmail.com                                                     #
#                                                                                           #
#############################################################################################

# basic functions for colormap

import numpy as np
import matplotlib.colors as clr


__all__ = ['colormap']

# List of all available colormaps
ColorMapList = ['Seismic', 'Phase', 'Frequency', 'Red-White-Blue', 'Gray',
                'Black-White-Red', 'Black-White-Green', 'Black-White-Blue',
                'White-Red-Black', 'White-Green-Black', 'White-Blue-Black',
                'Black-Red', 'Black-Green', 'Black-Blue']

# List of all available opacity optition
OpacityList = ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%',
               '___|\u207B\u207B\u207B', '\u207B\u207B\u207B|___',
               '__|\u207B\u207B|__', '\u207B\u207B|__|\u207B\u207B']


def makeOpacity(opacityname=None):
    if opacityname is None:
        opacityname = '100%'

    # default 100%
    opac = np.ones([2001, 1])

    # 0-100%
    if opacityname == '0%':
        opac = opac * 0.0
    if opacityname == '10%':
        opac = opac * 0.1
    if opacityname == '20%':
        opac = opac * 0.2
    if opacityname == '30%':
        opac = opac * 0.3
    if opacityname == '40%':
        opac = opac * 0.4
    if opacityname == '50%':
        opac = opac * 0.5
    if opacityname == '60%':
        opac = opac * 0.6
    if opacityname == '70%':
        opac = opac * 0.7
    if opacityname == '80%':
        opac = opac * 0.8
    if opacityname == '90%':
        opac = opac * 0.9
    if opacityname == '100%':
        opac = opac * 1.0

    # more opacity
    if opacityname == OpacityList[11]:
        opac[0:1001, :] = opac[0:1001, :] * 0.0
    if opacityname == OpacityList[12]:
        opac[1000:, :] = opac[1000:, :] * 0.0
    if opacityname == OpacityList[13]:
        opac[0:667, :] = opac[0:667, :] * 0.0
        opac[1334:, :] = opac[1334:, :] * 0.0
    if opacityname == OpacityList[14]:
        opac[667:1334, :] = opac[667:1334, :] * 0.0

    #
    return opac


def makeColorMap(cmapname=None, flip=False, opacity='100%', return_array=False):
    """
    Make common colormap used for data visualization
    Argus:
        cmapname:       name of colormap as listed below:
                            'Seismic', 'Phase', 'Frequency',
                            'Red-White-Blue',
                            'Black-White-Red', 'Black-White-Green', 'Black-White-Blue',
                            'Gray',
                            'White-Red-Black', 'White-Green-Black', 'White-Blue-Black',
                            'Black-Red', 'Black-Green', 'Black-Blue'
                            Default is 'Red-White-Blue'
        flip:           flip colormap or not
        opacity:        opacity
        return_array:   return cmap array if true; otherwise return ListedColorMap. Default is False.
    Return:
         colormap as listedcolormap object or 2D array
    """

    if cmapname is None:
        cmapname = 'Red-White-Blue'

    colormap = {}

    # alpha
    col_a = makeOpacity(opacity)

    # seismic
    col_loc = np.array([-1.0, -0.33, -0.2, 0.0, 0.2, 0.33, 1.0])
    col_r = np.array([161.0, 0.0, 77.0, 204.0, 97.0, 191.0, 255.0]) / 255.0
    col_g = np.array([255.0, 0.0, 77.0, 204.0, 69.0, 0.0, 255.0]) / 255.0
    col_b = np.array([255.0, 191.0, 77.0, 204.0, 0.0, 0.0, 0.0]) / 255.0
    col_r = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(-1.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    seismic = np.concatenate((col_r, col_g, col_b), axis=1)
    # Add to colormap dictionary
    colormap['Seismic'] = seismic

    # phase
    col_loc = np.linspace(0.0, 1.0, 11)
    col_r = np.array([255.0, 255.0, 255.0, 255.0, 198.0, 0.0, 0.0, 0.0, 0.0, 161.0, 255.0]) / 255.0
    col_g = np.array([0.0, 0.0, 114.0, 228.0, 255.0, 255.0, 255.0, 228.0, 114.0, 0.0, 0.0]) / 255.0
    col_b = np.array([255.0, 161.0, 0.0, 0.0, 0.0, 0.0, 198.0, 255.0, 255.0, 255.0, 255.0]) / 255.0
    col_r = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    phase = np.concatenate((col_r, col_g, col_b), axis=1)
    # Add to colormap dictionary
    colormap['Phase'] = phase

    # frequency
    col_loc = np.linspace(0.0, 1.0, 11)
    col_r = np.array([0.0, 255.0, 255.0, 240.0, 147.0, 0.0, 0.0, 0.0, 0.0, 170.0, 255.0]) / 255.0
    col_g = np.array([0.0, 0.0, 190.0, 255.0, 255.0, 255.0, 255.0, 208.0, 85.0, 0.0, 0.0]) / 255.0
    col_b = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 120.0, 225.0, 255.0, 255.0, 255.0, 255.0]) / 255.0
    col_r = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_r)
    col_g = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_g)
    col_b = np.interp(np.linspace(0.0, 1.0, 2001), col_loc, col_b)
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.reshape(col_b, [2001, 1])
    frequency = np.concatenate((col_r, col_g, col_b), axis=1)
    # Add to colormap dictionary
    colormap['Frequency'] = frequency

    # red_white_blue
    col_r = np.concatenate((np.ones([1001]), np.linspace(0.999, 0.0, 1000)))
    col_r = np.reshape(col_r, [2001, 1])
    col_g = np.concatenate((np.linspace(0.0, 1.0, 1001), np.linspace(0.999, 0.0, 1000)))
    col_g = np.reshape(col_g, [2001, 1])
    col_b = np.concatenate((np.linspace(0.0, 0.999, 1000), np.ones([1001])))
    col_b = np.reshape(col_b, [2001, 1])
    red_white_blue = np.concatenate((col_r, col_g, col_b), axis=1)
    # Add to colormap dictionary
    colormap['Red-White-Blue'] = red_white_blue

    # black_white_red/green/blue
    col_1 = np.concatenate((np.linspace(0.0, 0.999, 1000), np.ones([1001])))
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.concatenate((np.linspace(0.0, 1.0, 1001), np.linspace(0.999, 0.0, 1000)))
    col_2 = np.reshape(col_2, [2001, 1])
    black_white_red = np.concatenate((col_1, col_2, col_2), axis=1)
    black_white_green = np.concatenate((col_2, col_1, col_2), axis=1)
    black_white_blue = np.concatenate((col_2, col_2, col_1), axis=1)
    # Add to colormap dictionary
    colormap['Black-White-Red'] = black_white_red
    colormap['Black-White-Green'] = black_white_green
    colormap['Black-White-Blue'] = black_white_blue

    # white_gray_black
    col = np.linspace(1.0, 0.0, 2001)
    col = np.reshape(col, [2001, 1])
    white_gray_black = np.concatenate((col, col, col), axis=1)
    # Add to colormap dictionary
    colormap['Gray'] = white_gray_black

    # white_red/green/blue_black
    col_1 = np.concatenate((np.ones([1001]), np.linspace(0.999, 0.0, 1000)))
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.concatenate((np.linspace(1.0, 0.0, 1001), np.zeros([1000])))
    col_2 = np.reshape(col_2, [2001, 1])
    white_red_black = np.concatenate((col_1, col_2, col_2), axis=1)
    white_green_black = np.concatenate((col_2, col_1, col_2), axis=1)
    white_blue_black = np.concatenate((col_2, col_2, col_1), axis=1)
    # Add to colormap dictionary
    colormap['White-Red-Black'] = white_red_black
    colormap['White-Green-Black'] = white_green_black
    colormap['White-Blue-Black'] = white_blue_black

    # black_red/green/blue
    col_1 = np.linspace(0.0, 1.0, 2001)
    col_1 = np.reshape(col_1, [2001, 1])
    col_2 = np.zeros([2001])
    col_2 = np.reshape(col_2, [2001, 1])
    black_red = np.concatenate((col_1, col_2, col_2), axis=1)
    black_green = np.concatenate((col_2, col_1, col_2), axis=1)
    black_blue = np.concatenate((col_2, col_2, col_1), axis=1)
    # Add to colormap dictionary
    colormap['Black-Red'] = black_red
    colormap['Black-Green'] = black_green
    colormap['Black-Blue'] = black_blue

    cmapdata = colormap['Red-White-Blue']
    if cmapname in colormap:
        cmapdata = colormap[cmapname]
    if flip:
        cmapdata = np.flipud(cmapdata)

    cmapdata = np.concatenate((cmapdata, col_a), axis=1)

    if return_array:
        return cmapdata
    else:
        return clr.ListedColormap(cmapdata)


def applyColorMap(cmapmat=np.ones([100, 4]), vmin=-1.0, vmax=1.0, values=[1.0]):
    """
    Apply colormap to data
    Args:
        cmapmat:    2D colormap matrix of 3 or 4 columns
        vmin:       minimum value
        vmax:       maximum value
        values:     values as a list
    Return:
        2D colormap matrix for all values.
    """
    if np.ndim(cmapmat) != 2:
        print("ERROR in applyColorMap: 2D colormap matrix expected.")
        return None
    #
    nvalue = len(values)
    ncmp, ncom = np.shape(cmapmat)
    #
    cmp = np.zeros([nvalue, ncom])
    #
    for i in range(ncom):
        cmp[:, i] = np.interp(values, np.linspace(vmin, vmax, ncmp), cmapmat[:, i])
    #
    return  cmp


class colormap:
    # Pack all functions as a class
    #
    ColorMapList = ColorMapList
    OpacityList = OpacityList
    #
    makeColorMap = makeColorMap
    applyColorMap = applyColorMap