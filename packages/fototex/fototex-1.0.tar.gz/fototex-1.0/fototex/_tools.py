# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""

import multiprocessing as mp
import numpy as np
import time
from functools import partial

from sklearn.decomposition import IncrementalPCA
from tqdm import tqdm

from fototex import GDAL_FLOAT32, GDAL_DRIVER
from fototex._numba import get_radius, get_sectors
from fototex.foto_tools import rspectrum, split_into_chunks, pca, standard_deviation, rspectrum_per_sector


ISOTROPIC_R_SPECTRA_AXIS = 0
ANISOTROPIC_R_SPECTRA_AXIS = 1
ISOTROPIC_NB_SAMPLE_AXIS = 1
ANISOTROPIC_NB_SAMPLE_AXIS = 2


def incremental_pca(chunks, n_components, population_mean=None, population_std=None, nb_sectors=None):
    """ Incremental PCA

    :param chunks: iterator over data chunks
    :param n_components: number of dimensions for PCA
    :param population_mean: mean of the entire population from which is extracted each chunk
    :param population_std: std of the entire population from which is extracted each chunk
    :param nb_sectors: number of sectors (if None, no sectors)
    :return:
    """
    if nb_sectors is None:
        ipca = IncrementalPCA(n_components=n_components)
        axis = ISOTROPIC_R_SPECTRA_AXIS
    else:
        ipca = [IncrementalPCA(n_components=n_components)] * nb_sectors
        axis = ANISOTROPIC_R_SPECTRA_AXIS

    for chunk in chunks:

        if population_mean is None:
            chunk -= np.expand_dims(chunk.mean(axis=axis), axis=axis)
        else:
            chunk -= np.expand_dims(population_mean, axis=axis)

        if population_std is None:
            chunk /= np.expand_dims(chunk.std(axis=axis), axis=axis)
        else:
            chunk /= np.expand_dims(population_std, axis=axis)

        if nb_sectors:
            ipca = [ipca_.partial_fit(sub_chunk) for ipca_, sub_chunk in zip(ipca, chunk)]
        else:
            ipca.partial_fit(chunk)

    return ipca


def pca_transform(h5, eigen_vectors, chunk_size):
    """ Transform R-spectra to R-spectra reduced using given PCA eigen vectors

    :param h5: H5File with "r-spectra" dataset
    :param eigen_vectors: eigen vectors (numpy array)
    :param chunk_size: size of each chunk to be read and written
    :return:
    """
    nb_chunks = h5["r-spectra"].shape[0] // chunk_size + min(1, h5["r-spectra"].shape[0] % chunk_size)
    h5.reset_dataset("r-spectra-reduced", shape=(h5["r-spectra"].shape[0], eigen_vectors.shape[1]))
    for chunk in tqdm(h5.read("r-spectra", chunk_size), total=nb_chunks, desc="Reduce R-spectra"):
        h5.append("r-spectra-reduced", np.dot(chunk, eigen_vectors))


def pca_transform_sector():
    pass


def mp_h5_r_spectra(h5, window_gen, window_size, standardize, keep_dc_component, nb_rspectra, nb_sample, nb_processes,
                    chunk_size):
    """ Parallel processing of r-spectra with hdf5 storage

    :param h5: H5File
    :param window_gen: generator of windows
    :param window_size: window size
    :param standardize: (bool) standardization by the window's variance
    :param keep_dc_component: (bool) either keep or not the DC component of the FFT
    :param nb_rspectra: number of r-spectra to be computed
    :param nb_sample: number of sampled frequencies for each r-spectra
    :param nb_processes: number of processes to open
    :param chunk_size: size of each chunk to be saved into hdf5
    :return:
    """
    # Dataset
    h5.reset_dataset("r-spectra", (nb_rspectra, nb_sample))

    # Pixel coordinates within window
    y, x = np.indices((window_size, window_size))
    radius = get_radius(x, y)

    # For statistics computation (population mean and std)
    sum_of_values = np.zeros(nb_sample)
    sum_of_square_values = np.zeros(nb_sample)

    # Compute r-spectra chunk by chunk
    pg = tqdm(total=nb_rspectra // chunk_size + 1, desc="Compute R-spectra")
    for chk_nb, window_generator in enumerate(split_into_chunks(window_gen, chunk_size)):
        with mp.Pool(processes=nb_processes) as pool:
            r_spectra = np.asarray(list(pool.map(partial(rspectrum, radius=radius, window_size=window_size,
                                                         nb_sample=nb_sample, standardize=standardize,
                                                         keep_dc_component=keep_dc_component), window_generator,
                                                 chunksize=500)))
        sum_of_values += np.sum(r_spectra, axis=ISOTROPIC_R_SPECTRA_AXIS)
        sum_of_square_values += np.sum(r_spectra**2, axis=ISOTROPIC_R_SPECTRA_AXIS)
        h5.append("r-spectra", r_spectra)
        pg.update(1)
    pg.close()

    # Write dataset statistics to attributes
    h5["r-spectra"].attrs['mean'] = sum_of_values / nb_rspectra
    h5["r-spectra"].attrs['std'] = standard_deviation(nb_rspectra, sum_of_values, sum_of_square_values)

    # TODO: see if chunksize for Pool.map should not be fixed (500 here)


def mp_h5_r_spectra_sector(h5, window_gen, window_size, standardize, keep_dc_component, nb_rspectra, nb_sample,
                           nb_processes, chunk_size, nb_sectors):
    """ Parallel processing of anisotropic r-spectra with hdf5 storage

    :param h5:
    :param window_gen:
    :param window_size:
    :param standardize:
    :param keep_dc_component:
    :param nb_rspectra:
    :param nb_sample:
    :param nb_processes:
    :param chunk_size:
    :param nb_sectors:
    :return:
    """
    h5.reset_dataset("r-spectra", (nb_sectors, nb_rspectra, nb_sample))
    y, x = np.indices((window_size, window_size))
    radius = get_radius(x, y)
    sectors = get_sectors(x, y, nb_sectors)

    # Data used for population statistics
    sum_of_values = np.zeros((nb_sectors, nb_sample))
    sum_of_square_values = np.zeros((nb_sectors, nb_sample))

    # Compute r-spectra chunk by chunk
    pg = tqdm(total=nb_rspectra // chunk_size + 1, desc=f"Compute R-spectra for {nb_sectors} sectors")
    for chk_nb, window_generator in enumerate(split_into_chunks(window_gen, chunk_size)):
        with mp.Pool(processes=nb_processes) as pool:
            r_spectra = list(pool.map(partial(rspectrum_per_sector, radius=radius, sectors=sectors,
                                              window_size=window_size, nb_sample=nb_sample, nb_sectors=nb_sectors,
                                              standardize=standardize, keep_dc_component=keep_dc_component),
                                      window_generator, chunksize=500))
        r_spectra = np.transpose(np.asarray(r_spectra), (1, 0, 2))
        sum_of_values += np.sum(r_spectra, axis=ANISOTROPIC_R_SPECTRA_AXIS)
        sum_of_square_values += np.sum(r_spectra ** 2, axis=ANISOTROPIC_R_SPECTRA_AXIS)
        h5.append("r-spectra", r_spectra, axis=ANISOTROPIC_R_SPECTRA_AXIS)
        pg.update(1)
    pg.close()

    # Write dataset statistics to attributes
    h5["r-spectra"].attrs['mean'] = sum_of_values / nb_rspectra
    h5["r-spectra"].attrs['std'] = standard_deviation(nb_rspectra, sum_of_values, sum_of_square_values)


def mp_r_spectra(window_gen, window_size, standardize, keep_dc_component, nb_sample, nb_processes, nb_rspectra):
    """ Parallel processing of r-spectra

    :param window_gen: generator of windows
    :param window_size: size of the window
    :param standardize: (bool)
    :param keep_dc_component: (bool) either keep or not the DC component of the FFT
    :param nb_sample: number of sampled frequencies for each R-spectra
    :param nb_processes: number of processes to open for computation
    :param nb_rspectra: total number of r-spectra to compute
    :return:
    """
    # Pixel coordinates within window
    y, x = np.indices((window_size, window_size))
    radius = get_radius(x, y)

    # Parallel computation of r-spectra
    with mp.Pool(processes=nb_processes) as pool:
        r_spectra = list(tqdm(pool.imap(partial(rspectrum, radius=radius, window_size=window_size,
                                                nb_sample=nb_sample, standardize=standardize,
                                                keep_dc_component=keep_dc_component), window_gen, chunksize=500),
                              total=nb_rspectra, unit_scale=True, desc="Compute R-spectra"))

    return np.asarray(r_spectra)


def mp_r_spectra_sector(window_gen, window_size, standardize, keep_dc_component, nb_sample, nb_processes, nb_rspectra,
                        nb_sectors):
    """ Parallel processing of r-spectra

    :param window_gen: generator of windows
    :param window_size: size of the window
    :param standardize: (bool)
    :param keep_dc_component: (bool) either keep or not the DC component of the FFT
    :param nb_sample: number of sampled frequencies for each R-spectra
    :param nb_processes: number of processes to open for computation
    :param nb_rspectra: total number of r-spectra to compute
    :param nb_sectors: number of quadrants
    :return:
    """
    # Get radius and sectors within window
    y, x = np.indices((window_size, window_size))
    radius = get_radius(x, y)
    sectors = get_sectors(x, y, nb_sectors)

    # Parallel computation of r-spectra
    with mp.Pool(processes=nb_processes) as pool:
        r_spectra = list(tqdm(pool.imap(partial(rspectrum_per_sector, radius=radius, sectors=sectors,
                                                window_size=window_size, nb_sample=nb_sample, nb_sectors=nb_sectors,
                                                standardize=standardize, keep_dc_component=keep_dc_component),
                                        window_gen, chunksize=500), total=nb_rspectra, unit_scale=True,
                              desc=f"Compute anisotropic R-spectra for {nb_sectors} sectors"))
        r_spectra = np.transpose(np.asarray(r_spectra), (1, 0, 2))

    return r_spectra


def h5_incremental_pca(h5, n_components, chunk_size, at_random, batch_size, max_iter):
    """ Incremental PCA based on hdf5 dataset chunks

    :param h5: H5File
    :param n_components: number of components for PCA
    :param chunk_size: size of each chunk to be written
    :param at_random: read r-spectra batches at random (size of batch = batch_size)
    :param batch_size: size of batch when using read at random for incremental pca
    :param max_iter: maximum number of iterations if at_random=True
    :return:
    """
    nb_rspectra = h5["r-spectra"].shape[ISOTROPIC_R_SPECTRA_AXIS]
    nb_chunks = nb_rspectra // chunk_size + min(1, nb_rspectra % chunk_size)
    population_mean = h5["r-spectra"].attrs["mean"]
    population_std = h5["r-spectra"].attrs["std"]

    if at_random:
        if batch_size is None:
            batch_size = h5["r-spectra"].shape[ISOTROPIC_NB_SAMPLE_AXIS] * 2**3
        r_spectra_generator = h5.read_at_random("r-spectra", batch_size)
        nb_iterations = max_iter
    else:
        r_spectra_generator = h5.read("r-spectra", chunk_size)
        nb_iterations = nb_chunks

    # Incremental PCA
    # Read R-spectra by chunk or batch (if at random) and partial fit
    chunks = tqdm(r_spectra_generator, total=nb_iterations, desc="Compute Incremental PCA")
    ipca = incremental_pca(chunks, n_components, population_mean, population_std)

    # Finalization
    # Write R-spectra reduced to hdf5 dataset
    h5.reset_dataset("r-spectra-reduced", shape=(nb_rspectra, n_components))
    for chunk in tqdm(h5.read("r-spectra", chunk_size), total=nb_chunks, desc="Store R-spectra reduced"):
        chunk -= population_mean
        chunk /= population_std
        h5.append("r-spectra-reduced", ipca.transform(chunk))

    return ipca.components_.T


def h5_incremental_pca_sector(h5, n_components, chunk_size, at_random, batch_size, max_iter, nb_sectors):
    """

    :param h5:
    :param n_components:
    :param chunk_size:
    :param at_random:
    :param batch_size:
    :param max_iter:
    :param nb_sectors:
    :return:
    """
    nb_rspectra = h5["r-spectra"].shape[ANISOTROPIC_R_SPECTRA_AXIS]
    nb_chunks = nb_rspectra // chunk_size + min(1, nb_rspectra % chunk_size)
    population_mean = h5["r-spectra"].attrs["mean"]
    population_std = h5["r-spectra"].attrs["std"]

    if at_random:
        if batch_size is None:
            batch_size = h5["r-spectra"].shape[ANISOTROPIC_NB_SAMPLE_AXIS] * 2**3
        r_spectra_generator = h5.read_at_random("r-spectra", batch_size, axis=ANISOTROPIC_R_SPECTRA_AXIS)
        nb_iterations = max_iter
    else:
        r_spectra_generator = h5.read("r-spectra", chunk_size, axis=ANISOTROPIC_R_SPECTRA_AXIS)
        nb_iterations = nb_chunks

    # Incremental PCA
    # Read R-spectra by chunk or batch (if at random) and partial fit
    chunks = tqdm(r_spectra_generator, total=nb_iterations,
                  desc=f"Compute Incremental PCA for each of the {nb_sectors} sectors")
    ipca = incremental_pca(chunks, n_components, population_mean, population_std, nb_sectors)

    # Finalization
    # Write R-spectra reduced to hdf5 dataset
    h5.reset_dataset("r-spectra-reduced", shape=(nb_sectors, nb_rspectra, n_components))
    for chunk in tqdm(h5.read("r-spectra", chunk_size, axis=ANISOTROPIC_R_SPECTRA_AXIS),
                      total=nb_chunks, desc=f"Store R-spectra reduced for {nb_sectors} sectors"):
        chunk -= np.expand_dims(population_mean, axis=ANISOTROPIC_R_SPECTRA_AXIS)
        chunk /= np.expand_dims(population_std, axis=ANISOTROPIC_R_SPECTRA_AXIS)
        ipca_transform = np.asarray([ipca_.transform(chunk_) for ipca_, chunk_ in zip(ipca, chunk)])
        h5.append("r-spectra-reduced", ipca_transform, axis=ANISOTROPIC_R_SPECTRA_AXIS)

    return [ipca_.components_.T for ipca_ in ipca]


def normal_pca(r_spectra, n_components):
    """ Normal PCA

    :param r_spectra: table of r-spectra
    :param n_components: number of dimensions for PCA
    :return:
    """
    def _tqdm_pca():
        bar_length = r_spectra.size // 100
        pg = tqdm(total=bar_length, desc="Compute PCA", unit_scale=True)
        for i in range(int(bar_length)):
            pg.update(1)
            time.sleep(0.0001)
            if quit_process.is_set():
                break
        pg.n = bar_length
        pg.refresh()
        pg.close()

    quit_process = mp.Event()
    p = mp.Process(target=_tqdm_pca)
    p.start()

    eigen_vectors, r_spectra_reduced = pca(r_spectra, n_components, True)

    # Stop PCA process
    quit_process.set()
    p.join()

    return eigen_vectors, r_spectra_reduced


def normal_pca_sector(r_spectra, n_components, nb_sectors):
    """ Compute PCA for each quadrant

    :param r_spectra:
    :param n_components:
    :param nb_sectors:
    :return:
    """
    def _tqdm_pca():
        bar_length = nb_sectors * r_spectra.size // 100
        pg = tqdm(total=bar_length, desc=f"Compute PCA for {nb_sectors} sectors", unit_scale=True)
        for i in range(int(bar_length)):
            pg.update(1)
            time.sleep(0.0001)
            if quit_process.is_set():
                break
        pg.n = bar_length
        pg.refresh()
        pg.close()

    quit_process = mp.Event()
    p = mp.Process(target=_tqdm_pca)
    p.start()

    results = [pca(rspec, n_components, True) for rspec in r_spectra]

    # Stop PCA process
    quit_process.set()
    p.join()

    return [result[0] for result in results], [result[1] for result in results]


def out_raster_dataset(input_dataset, method, window_size, path_to_rgb, raster_width, raster_height, n_bands):
    """ Get output raster gdal dataset to which later write r-spectra reduced data

    :param input_dataset: input GDAL dataset from which must be created the output raster dataset
    :param method: string in {"block", "moving_window"}
    :param window_size: size of the window for Foto computation
    :param path_to_rgb: path to the raster file
    :param raster_width: width (in pixel) of the raster
    :param raster_height: height (in pixel) of the raster
    :param n_bands: number of bands of the raster
    :return:
    """
    out_dataset = GDAL_DRIVER.Create(path_to_rgb, raster_width, raster_height, n_bands, GDAL_FLOAT32)
    if method == "block":
        topleftx, pxsizex, rotx, toplefty, roty, pxsizey = input_dataset.GetGeoTransform()
        out_dataset.SetGeoTransform((topleftx, pxsizex * window_size, rotx, toplefty, roty, pxsizey * window_size))
    else:
        out_dataset.SetGeoTransform(input_dataset.GetGeoTransform())
    out_dataset.SetProjection(input_dataset.GetProjection())

    return out_dataset


def write_rgb(in_dataset, out_dataset, r_spectra_reduced, n_components):
    """ Write RGB image to raster file using gdal

    Write image to raster line by line
    :param in_dataset: gdal dataset of original image
    :param out_dataset: gdal output RGB dataset
    :param r_spectra_reduced: r-spectra after PCA (numpy array of h5 dataset)
    :param n_components: number of components of PCA (equal to number of band of RGB output image)
    :return:
    """

    row_width = out_dataset.RasterXSize
    for y in tqdm(range(0, out_dataset.RasterYSize), desc=f"Saving RGB output image to {out_dataset.GetDescription()}",
                  unit_scale=True):
        for band in range(n_components):
            rgb = np.expand_dims(r_spectra_reduced[y*row_width:(y+1)*row_width, band], axis=0)
            out_dataset.GetRasterBand(band + 1).WriteArray(rgb, 0, y)
