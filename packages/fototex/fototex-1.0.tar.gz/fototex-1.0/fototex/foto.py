# -*- coding: utf-8 -*-

""" FOTO main module.

Main module of FOTO algorithm. Defines FotoBase class and inherited classes.
"""

import itertools
import multiprocessing as mp
import os
from abc import abstractmethod

import gdal
import numpy as np
from utils.check import check_string, lazyproperty, check_type_in_collection

from fototex import NB_PCA_COMPONENTS, MAX_NB_OF_SAMPLED_FREQUENCIES
from fototex._tools import mp_r_spectra, mp_h5_r_spectra, normal_pca, h5_incremental_pca, write_rgb, \
    out_raster_dataset, pca_transform, normal_pca_sector, mp_r_spectra_sector, mp_h5_r_spectra_sector, \
    h5_incremental_pca_sector
from fototex.exceptions import FotoBaseError, FotoBatchError, FotoError, FotoSectorBatchError
from fototex._numba import get_block_windows, get_moving_windows
from fototex.foto_tools import degrees_to_cardinal
from fototex.io import H5TempFile, H5File


# TODO: add standardize and keep_dc_component options in path names ?
class FotoBase:
    """ Foto base class

    Main Foto abstract class for all Foto subclasses
    """
    _r_spectra = None
    _r_spectra_reduced = None

    out_dir = None
    method = None
    max_nb_sampled_frequencies = MAX_NB_OF_SAMPLED_FREQUENCIES
    nb_pca_components = NB_PCA_COMPONENTS
    window_size = None
    nb_sampled_frequencies = None
    standardize = None
    keep_dc_component = None
    eigen_vectors = None

    def __init__(self, out_dir, method, in_memory, data_chunk_size, *args, **kwargs):
        """ FotoBase class constructor

        Description
        -----------

        Parameters
        ----------
        :param out_dir: (path str) output directory for writing results
        :param method: (str) window method used in the algorithm ("block" or "moving_window")
        :param in_memory: (bool) either run FOTO in memory or using HDF5 file storage on the fly
        :param data_chunk_size: (int) when using HDF5 storage, number of data per chunk
        :param args:
        :param kwargs:
        """
        if not os.path.isdir(out_dir):
            raise FotoBaseError(f"{out_dir} is not a valid directory path")
        else:
            self.out_dir = out_dir

        self.method = check_string(method, {'block', 'moving_window'})
        self.in_memory = in_memory
        self.data_chunk_size = data_chunk_size

    @abstractmethod
    def _get_window_generator(self):
        pass

    def _compute_r_spectra(self, nb_processes, *args, **kwargs):
        if self.in_memory:
            self._r_spectra = mp_r_spectra(self._get_window_generator(), self.window_size, self.standardize,
                                           self.keep_dc_component, self.nb_sampled_frequencies, nb_processes,
                                           self.nb_windows)
        else:
            mp_h5_r_spectra(self.h5, self._get_window_generator(), self.window_size, self.standardize,
                            self.keep_dc_component, self.nb_windows, self.nb_sampled_frequencies, nb_processes,
                            self.chunk_size)

    def compute_pca(self, at_random=False, batch_size=None, max_iter=1000, *args, **kwargs):
        """ Compute PCA for r-spectra tables

        Description
        -----------
        Reduce dimensionality of r-spectra table, with
        respect to number of components (by default set
        to 3 for RGB maps calculation), by applying
        principal component analysis (PCA)

        Parameters
        ----------
        :param at_random: apply random incremental pca
        :param batch_size: size of batch for random incremental pca if at_random=True
        :param max_iter: maximum number of iterations if at_random=True

        :return: reduced r-spectra table and corresponding eigen vectors
        """
        if self.in_memory:
            self.eigen_vectors, self._r_spectra_reduced = normal_pca(self._r_spectra, self.nb_pca_components)
        else:
            self.eigen_vectors = h5_incremental_pca(self.h5, self.nb_pca_components, self.chunk_size, at_random,
                                                    batch_size, max_iter)

    def compute_r_spectra(self, window_size, nb_of_sampled_frequencies=None, standardize=False, keep_dc_component=False,
                          nb_processes=mp.cpu_count(), *args, **kwargs):
        """ Compute r-spectra over image with respect to method

        Description
        -----------
        Compute rspectra tables for given image,
        depending on the selected method and other
        parameters (window size, standardization, etc.)

        Parameters
        ---------
        :param window_size: size of window
        :param nb_of_sampled_frequencies: number of sampled frequencies
        :param standardize: (bool) standardize by window variance
        :param keep_dc_component: (bool) keep the DC component (0 frequency) of the FFT. Use carefully as it may
        substantially change the final results!
        :param nb_processes: number of processes for multiprocessing calculation

        Returns
        -------
        :return: current instance with computed r-spectra
        """
        # Set window size and standardize bool
        self.window_size = window_size
        self.standardize = standardize
        self.keep_dc_component = keep_dc_component

        if not nb_of_sampled_frequencies:
            self.nb_sampled_frequencies = min(max(int(window_size / 2), 3), self.max_nb_sampled_frequencies)
        else:
            self.nb_sampled_frequencies = nb_of_sampled_frequencies

        self._compute_r_spectra(nb_processes)

    def fit_transform(self, other, nb_processes=mp.cpu_count(), *args, **kwargs):
        """ Apply eigen vectors from other Foto object to current object's R-spectra

        Description
        -----------
        Use the PCA eigen vectors retrieved from
        another FotoBase class that has been run
        in order to get reduced r-spectra for the
        current instance

        Required parameters
        -------------------
        :param other: Foto class instance that have been run

        Optional parameters
        -------------------
        :param nb_processes: (int) number of processes to open for multiprocessing

        Returns
        -------
        :return:
        """
        # TODO: prototype method (apply eigen vectors computed from some image to another)

        # Compute r-spectra and project in input Foto eigenvector's base
        self.compute_r_spectra(other.window_size, other.nb_sample, other.standardize, nb_processes)

        if self.in_memory:
            self._r_spectra_reduced = np.dot(self._r_spectra, other.eigen_vectors)
        else:
            self._r_spectra_reduced = pca_transform(self.h5, other.eigen_vectors, self.chunk_size)

    def run(self, window_size, nb_of_sampled_frequencies=None, standardize=False, keep_dc_component=False,
            at_random=False, batch_size=None, max_iter=1000, nb_processes=mp.cpu_count(), *args, **kwargs):
        """ Run FOTO algorithm

        Description
        -----------
        Run the whole FOTO algorithm, consisting
        in computing r-spectra and applying PCA,
        with respect to window size and corresponding
        method ("block" or "moving window")

        Parameters
        ----------
        :param window_size: (int number) size of the window for 2-D FFT (must be an odd number when method = "moving")
        :param nb_of_sampled_frequencies: number of sampled frequencies (if None, is inferred)
        :param standardize: (bool) standardize power spectrum density by window's variance
        :param keep_dc_component: (bool) either keep or not the DC component (0 frequency) part of the signal FFT.
        Use carefully as it may change substantially the final results !
        :param nb_processes: (int) number of processes for parallelization
        :param at_random: if True, use random incremental pca
        :param batch_size: size of batch for random incremental pca (if None, batch size is inferred)
        :param max_iter: maximum number of iterations when using random incremental PCA

        Returns
        -------
        :return:
        """
        self.compute_r_spectra(window_size, nb_of_sampled_frequencies, standardize, keep_dc_component, nb_processes)
        self.compute_pca(at_random, batch_size, max_iter)

    def save_eigen_vectors(self):
        """ Save eigen vectors computed with PCA

        Description
        -----------
        Write eigen vectors retrieved from PCA
        to csv file

        Returns
        -------
        :return:
        """
        np.savetxt(self.path + "eigen_vectors.csv", self.eigen_vectors, delimiter=',')

    def save_r_spectra(self):
        """ Save r-spectra table to h5 file

        Description
        -----------
        Write computed r-spectra to H5 file

        Returns
        -------
        :return:
        """
        h5file = H5File(self.path + "rpsectra.h5")
        if self.in_memory:
            h5file.create_dataset("r-spectra", shape=self._r_spectra.shape)
            h5file.append("r-spectra", self._r_spectra)
        else:
            h5file.copy(self.h5, "r-spectra")

        h5file.close()

    @property
    def chunk_size(self):
        return int(self.data_chunk_size / self.nb_sampled_frequencies)

    @lazyproperty
    def h5(self):
        if not self.in_memory:
            return H5TempFile()

    @property
    @abstractmethod
    def nb_windows(self):
        pass

    @property
    def path(self):
        return os.path.join(self.out_dir, f"method={self.method}_wsize={self.window_size}_")

    @property
    def r_spectra(self):
        if self.in_memory:
            return self._r_spectra
        else:
            return self.h5["r-spectra"]

    @property
    def r_spectra_reduced(self):
        if self.in_memory:
            return self._r_spectra_reduced
        else:
            return self.h5["r-spectra-reduced"]


class Batch(FotoBase):
    """ Batch class

    Batch is used to allow applying the FOTO
    algorithm from multiple image batches
    """

    def __init__(self, out_dir, method, in_memory, data_chunk_size, foto_collection=None):
        """ Batch instance constructor

        Description
        -----------
        This class should not be used, but be
        inherited by subclasses that must implement
        the batch process, especially by using
        multiple inheritance

        Parameters
        ----------
        :param out_dir:
        :param method:
        :param in_memory:
        :param data_chunk_size:
        :param foto_collection: collection of FotoBase instances
        """

        self.foto_instances = foto_collection
        super().__init__(out_dir, method, in_memory, data_chunk_size)

    def _get_window_generator(self):
        w_gen = []
        for foto in self.foto_instances:
            w_gen.append(foto._get_window_generator())

        return itertools.chain(*w_gen)

    @property
    def nb_windows(self):
        nb_rspec = 0
        for foto in self.foto_instances:
            nb_rspec += foto.nb_windows
        return nb_rspec


class Sector(FotoBase):
    """ Sector abstract method to implement anisotropy within FOTO algorithm

    """

    def __init__(self, out_dir, method="block", in_memory=True, data_chunk_size=50000, nb_sectors=6):
        """ Sector constructor

        Description
        -----------
        Sector should not be used by itself.
        This class must be inherited by subclasses
        that implement anisotropy.

        Required parameters
        -------------------
        :param out_dir:

        Optional parameters
        -------------------
        :param method:
        :param in_memory:
        :param data_chunk_size:
        :param nb_sectors:

        Note
        ----
        In order to correctly override FotoBase and use Sector with
        other subclasses of FotoBase, we must keep the constructor
        syntax order. That is to put "nb_sectors" at the end. In case
        we later use multiple inheritance, it is very important so that
        there is no conflict between multiple constructors inheriting
        from the same superclass (here FotoBase)
        """
        self.nb_sectors = nb_sectors
        super().__init__(out_dir, method, in_memory, data_chunk_size)

    def _compute_r_spectra(self, nb_processes, *args, **kwargs):
        if self.in_memory:
            self._r_spectra = mp_r_spectra_sector(self._get_window_generator(), self.window_size, self.standardize,
                                                  self.keep_dc_component, self.nb_sampled_frequencies,
                                                  nb_processes, self.nb_windows, self.nb_sectors)
        else:
            self._r_spectra = mp_h5_r_spectra_sector(self.h5, self._get_window_generator(), self.window_size,
                                                     self.standardize, self.keep_dc_component, self.nb_windows,
                                                     self.nb_sampled_frequencies, nb_processes, self.chunk_size,
                                                     self.nb_sectors)

    def compute_pca(self, at_random=False, batch_size=None, max_iter=1000, *args, **kwargs):
        """ Compute PCA for each rspectra tables per sector

        Description
        -----------
        For each r-spectra table corresponding to a given
        sector, reduce the dimensionality by applying a
        PCA.

        Parameters
        ----------
        :param at_random:
        :param batch_size:
        :param max_iter:

        :return: FotoSector object with reduced r-spectra and corresponding eigen vectors
        """
        if self.in_memory:
            self.eigen_vectors, self._r_spectra_reduced = normal_pca_sector(self._r_spectra, self.nb_pca_components,
                                                                            self.nb_sectors)
        else:
            self.eigen_vectors = h5_incremental_pca_sector(self.h5, self.nb_pca_components, self.chunk_size,
                                                           at_random, batch_size, max_iter, self.nb_sectors)

    def save_eigen_vectors(self):
        """ Save eigen vectors from PCA decomposition

        Description
        -----------

        Returns
        -------
        :return:
        """
        for path, eigen_vectors in zip(self.path, self.eigen_vectors):
            np.savetxt(path + "eigen_vectors.csv", eigen_vectors, delimiter=',')

    @property
    def chunk_size(self):
        return int(self.data_chunk_size / (self.nb_sampled_frequencies * self.nb_sectors))

    @property
    def sectors(self):
        sectors = [sector * 360 // self.nb_sectors for sector in range(self.nb_sectors)]
        return sectors[self.nb_sectors // 2 + 1:] + sectors[:self.nb_sectors // 2 + 1]

    @abstractmethod
    def _get_window_generator(self):
        pass

    @property
    @abstractmethod
    def nb_windows(self):
        pass


class Foto(FotoBase):
    """ Foto class instance

    Foto object allows to run the Foto algorithm (Couteron et al., 2006) on
    any kind of raster.
    """

    def __init__(self, image, band=None, method="block", in_memory=True, data_chunk_size=50000):
        """ Foto class constructor

        Description
        -----------
        Build a Foto object on which might
        later be run the algorithm. It is
        specifically designed to run on one
        image.

        Required parameter
        ------------------
        :param image: path to raster file (must be gdal readable)

        Optional parameters
        -------------------
        :param band: band number if multi-band raster
        :param method: method for window analysis ("block" or "moving")
        :param in_memory: (bool) if true, import whole raster or band as numpy array
        :param data_chunk_size: size (nb of elements) of a chunk of data to load in memory (if in_memory == False)
        """
        self.band = band
        try:
            self.dataset = gdal.Open(image, gdal.GA_ReadOnly)
        except RuntimeError as e:
            raise FotoError(e)
        super().__init__(self.image_dir, method, in_memory, data_chunk_size)

    def _get_window_generator(self):
        """ Create window generator depending on the given memory method

        :return: window generator
        """
        if self.in_memory:
            return (self.image[w[1]:w[1] + w[3], w[0]:w[0] + w[2]] for w in self.windows)
        else:
            if self.band:
                band_array = self.dataset.GetRasterBand(self.band)
                return (band_array.ReadAsArray(*window) for window in self.windows)
            else:
                return (self.dataset.ReadAsArray(*window) for window in self.windows)

    def save_rgb(self):
        """ Save RGB image to file using gdal

        Description
        -----------
        Save reduced r-spectra table to RGB map

        Returns
        -------
        :return:
        """
        out_dataset = out_raster_dataset(self.dataset, self.method, self.window_size, self.rgb_file,
                                         self.rgb_width, self.rgb_height, self.nb_pca_components)

        write_rgb(self.dataset, out_dataset, self.r_spectra_reduced, self.nb_pca_components)

    @property
    def nb_windows(self):
        return self.rgb_height * self.rgb_width

    @lazyproperty
    def image(self):
        if self.in_memory:
            if self.band:
                return self.dataset.GetRasterBand(self.band).ReadAsArray()
            else:
                return self.dataset.ReadAsArray()

    @property
    def image_dir(self):
        return os.path.dirname(self.dataset.GetDescription())

    @property
    def image_name(self):
        return os.path.splitext(os.path.split(self.dataset.GetDescription())[1])[0]

    @property
    def path(self):
        return os.path.join(self.out_dir, f"{self.image_name}_method={self.method}_wsize={self.window_size}_")

    @property
    def rgb_file(self):
        return self.path + "rgb.tif"

    @property
    def rgb_width(self):
        if self.method == "block":
            return int(self.dataset.RasterXSize / self.window_size) + \
                   min(1, self.dataset.RasterXSize % self.window_size)
        else:
            return self.dataset.RasterXSize

    @property
    def rgb_height(self):
        if self.method == "block":
            return int(self.dataset.RasterYSize / self.window_size) + \
                   min(1, self.dataset.RasterYSize % self.window_size)
        else:
            return self.dataset.RasterYSize

    @property
    def windows(self):
        if self.method == 'block':
            return get_block_windows(self.window_size, self.dataset.RasterXSize, self.dataset.RasterYSize)
        else:
            return get_moving_windows(self.window_size, self.dataset.RasterXSize, self.dataset.RasterYSize)


class FotoBatch(Batch):
    """ FotoBatch class

    FotoBatch allows for supplying image batches to the Foto algorithm
    """

    def __init__(self, out_dir, foto_collection, method="block", in_memory=True, data_chunk_size=50000):
        """ Build FotoBatch instance

        Description
        -----------
        FotoBatch instance allows for applying the
        FOTO algorithm on multiple images (batches)

        Required parameters
        ----------
        :param out_dir: path to directory where saving outputs
        :param foto_collection: collection of Foto instances

        Optional parameters
        -------------------
        :param method: (str) window method {'block' or 'moving_window'}
        :param in_memory: (bool) either implement FOTO in memory or using HDF5 file storage on the fly
        :param data_chunk_size: (int) if HDF5 storage is implemented, number of data per chunk
        """
        super().__init__(out_dir, method, in_memory, data_chunk_size, foto_collection)

        # Store Foto instances of images
        try:
            check_type_in_collection(foto_collection, Foto)
            self.foto_instances = foto_collection
        except TypeError as e:
            raise FotoBatchError(e)

    def compute_r_spectra(self, window_size, nb_of_sampled_frequencies=None, standardize=False, keep_dc_component=False,
                          nb_processes=mp.cpu_count(), *args, **kwargs):
        """ Compute r-spectra tables for all batches

        Description
        -----------
        Compute r-spectra table from all supplied
        image batches

        Required parameters
        -------------------
        :param window_size:

        Optional parameters
        -------------------
        :param nb_of_sampled_frequencies:
        :param standardize:
        :param keep_dc_component:
        :param nb_processes:
        :param args:
        :param kwargs:

        Returns
        -------
        :return:
        """
        for foto in self.foto_instances:
            foto.window_size = window_size
        super().compute_r_spectra(window_size, nb_of_sampled_frequencies, standardize, keep_dc_component, nb_processes)


class FotoSector(Foto, Sector):

    def __init__(self, image, nb_sectors=6, band=None, method="block", in_memory=True, data_chunk_size=50000):
        """ FotoSector constructor

        Description
        -----------
        FotoSector apply the anisotropic version
        of the FOTO algorithm. Typically, depending
        on the required number of sectors, r-spectra
        will be computed for each sector, i.e. circle
        division.

        Required parameters
        -------------------
        :param image:

        Optional parameters
        -------------------
        :param nb_sectors:
        :param band:
        :param method:
        :param in_memory:
        :param data_chunk_size:

        Note
        ----
        We use here the feature of multiple inheritance,
        by building FotoSector as the mixin of Foto and
        Sector. Look at the Note in Sector to understand
        how to avoid typical issues when doing this. Here,
        Foto and Sector both inherit from FotoBase, as a result
        we must take care of the argument order in the constructor
        of both Foto and Sector classes.
        """
        Foto.__init__(self, image, band, method, in_memory, data_chunk_size)
        Sector.__init__(self, self.image_dir, method, in_memory, data_chunk_size, nb_sectors)

    def save_rgb(self):
        """ Save RGB image corresponding to each sector

        Description
        -----------
        Save RGB image from reduced r-spectra, one for
        each corresponding sector

        Returns
        -------
        :return:
        """
        for path, r_spectra_reduced in zip(self.path, self.r_spectra_reduced):
            out_dataset = out_raster_dataset(self.dataset, self.method, self.window_size, path + "rgb.tif",
                                             self.rgb_width, self.rgb_height, self.nb_pca_components)

            write_rgb(self.dataset, out_dataset, r_spectra_reduced, self.nb_pca_components)

    @property
    def path(self):
        new_path = super().path
        return [new_path + f"sector={sector}_{degrees_to_cardinal(sector)}_" for sector in self.sectors]


class FotoSectorBatch(FotoBatch, Sector):

    def __init__(self, out_dir, foto_collection, nb_sectors=6, method="block", in_memory=True, data_chunk_size=50000):
        """ FotoSectorBatch

        Description
        -----------
        Run FOTO anisotropic algorithm from
        image batches

        Required parameters
        -------------------
        :param out_dir:
        :param foto_collection:

        Optional parameters
        -------------------
        :param nb_sectors:
        :param method:
        :param in_memory:
        :param data_chunk_size:
        """
        FotoBatch.__init__(self, out_dir, foto_collection, method, in_memory, data_chunk_size)
        Sector.__init__(self, out_dir, nb_sectors=nb_sectors)

        try:
            check_type_in_collection(foto_collection, FotoSector)
        except TypeError as e:
            raise FotoSectorBatchError(e)
