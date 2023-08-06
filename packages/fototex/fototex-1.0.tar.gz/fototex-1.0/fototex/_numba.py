# -*- coding: utf-8 -*-

""" Module gathering all numba-based optimized functions

We preferentially use numba jit decorator without signature. As detailed
in the numba documentation in that case:
"The decorated function implements lazy compilation.
Each call to the decorated function will try to re-use an existing
specialization if it exists (for example, a call with two integer
arguments may re-use a specialization for argument types
(numba.int64, numba.int64)). If no suitable specialization exists,
a new specialization is compiled on-the-fly, stored for later use,
and executed with the converted arguments."
"""

import numpy as np

from numba import jit, int64


# @jit([float64[:](int64[:], float64[:]), ], nopython=True, nogil=True)
@jit(nopython=True, nogil=True)
def get_average_per_radius(radius, values):
    """

    :param radius:
    :param values:
    :return:
    """
    return np.bincount(radius, values) / np.bincount(radius)


# @jit(float64[:, :](float64[:, :], int64[:], int64[:], int64), nopython=True, nogil=True)
@jit(nopython=True, nogil=True)
def sector_average(window, radius, sectors, nb_sectors):
    window = window.ravel()
    r_average_per_sector = np.zeros((nb_sectors, radius.max() + 1))
    for sector in np.unique(sectors):
        mask = np.where(sectors == sector)
        average = get_average_per_radius(radius[mask], window[mask])
        r_average_per_sector[sector - 1, 0:average.size] = average

    r_average_per_sector[:, 0] = r_average_per_sector[~np.isnan(r_average_per_sector[:, 0]), 0]

    return r_average_per_sector


# @jit([float64[:](int64[:], float64[:, :]), float32[:](int64[:], float32[:, :])], nopython=True, nogil=True)
@jit(nopython=True, nogil=True)
def azimuthal_average(radius, window):

    return get_average_per_radius(radius, window.ravel())


@jit(nopython=True)
def azimuthal_max(x, y, window):
    radius = get_radius(x, y)

    return get_max_per_radius(radius, window)


# TODO: succeed in using numba and optimizing get_max_per_radius function
# @jit(nopython=True)
def get_max_per_radius(radius, values):
    """

    :param radius:
    :param values:
    :return:
    """
    return np.asarray([values[radius == r].max() for r in np.unique(radius)])


# @jit(float64[:, :](int64[:, :], int64[:, :]), nopython=True, nogil=True)
@jit(nopython=True, nogil=True)
def get_azimuth(x, y):
    """ Return azimuth of all window pixels with respect to window origin

    :param x: pixel x coordinates as returned by np.indices function
    :param y: pixel y coordinates as returned by np.indices function
    :return:
    """
    return np.arctan2(x - (x.shape[1] - 1) / 2, (y.shape[0] - 1) / 2 - y)


@jit(nopython=True, nogil=True)
def get_bin_sectors(nb_bins):
    """ Return bin circle sectors from required number of bins

    Return bin sectors centered on O° (i.e. North)
    :param nb_bins: (integer) number of bins
    :return:
    """
    bin_quadrants = np.linspace(-(nb_bins - 1) * np.pi / nb_bins, (nb_bins - 1) * np.pi / nb_bins, nb_bins)
    if nb_bins % 2 == 0:
        return bin_quadrants
    else:
        return bin_quadrants + np.pi/nb_bins


@jit(nopython=True)
def get_block_windows(window_size, raster_x_size, raster_y_size):
    """ Get block window coordinates

    Get block window coordinates depending
    on raster size and window size
    :param window_size:
    :param raster_x_size:
    :param raster_y_size:
    :return:
    """
    for y in range(0, raster_y_size, window_size):
        ysize = min(window_size, raster_y_size - y)
        for x in range(0, raster_x_size, window_size):
            xsize = min(window_size, raster_x_size - x)

            yield x, y, xsize, ysize


@jit(nopython=True)
def get_moving_windows(window_size, raster_x_size, raster_y_size, step=1):
    """ Get moving window coordinates

    Get moving window coordinates depending
    on raster size, window size and step
    :param window_size:
    :param raster_x_size:
    :param raster_y_size:
    :param step:
    :return:
    """
    offset = int((window_size - 1) / 2)  # window_size must be an odd number
    # for each pixel, compute indices of the window (all included)
    for y in range(0, raster_y_size, step):
        y1 = max(0, y - offset)
        y2 = min(raster_y_size - 1, y + offset)
        ysize = (y2 - y1) + 1
        for x in range(0, raster_x_size, step):
            x1 = max(0, x - offset)
            x2 = min(raster_x_size - 1, x + offset)
            xsize = (x2 - x1) + 1

            yield x1, y1, xsize, ysize


@jit(nopython=True, nogil=True)
def get_sectors(x, y, nb_sectors):
    sectors = np.digitize(get_azimuth(x, y), get_bin_sectors(nb_sectors))
    sectors = sectors.ravel()
    mask = np.where(sectors == 0)
    sectors[mask] = nb_sectors

    return sectors


@jit(nopython=True, nogil=True)
def get_radius(x, y):
    """ Return radius of window pixels with respect to window origin

    :param x: pixel x coordinates
    :param y: pixel y coordinates
    :return:
    """
    radius = np.sqrt((x - (x.shape[1] - 1) / 2) ** 2 + (y - (x.shape[0] - 1) / 2) ** 2).astype(int64)

    return radius.ravel()
