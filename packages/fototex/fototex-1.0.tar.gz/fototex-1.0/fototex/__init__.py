# -*- coding: utf-8 -*-

""" Compute Fourier Transform Textural Ordination.

FOTO algorithm package by and for python. Use to retrieve
textural information in satellite images.

- Example of usage:
>>> from fototex.foto import Foto
>>> foto = Foto("/path/to/image.tif", method="moving_window")
>>> foto.run(window_size=11)

"""

__version__ = '1.0'
__licence__ = "MIT"

import gdal

# Raise Python exceptions for gdal errors
gdal.UseExceptions()

# Main variables
GDAL_DRIVER = gdal.GetDriverByName("GTiff")
GDAL_FLOAT32 = gdal.GetDataTypeByName('Float32')
NB_PCA_COMPONENTS = 3
MAX_NB_OF_SAMPLED_FREQUENCIES = 29
