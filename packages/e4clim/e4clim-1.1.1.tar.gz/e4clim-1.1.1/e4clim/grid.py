"""Gridded-data base definitions."""
import os
from copy import deepcopy
from abc import ABC, abstractmethod
import numpy as np
import xarray as xr
from scipy.spatial import cKDTree
from .data_source import DataSourceLoaderBase


class GriddedDataSourceBase(DataSourceLoaderBase, ABC):
    """Gridded data-source abstract base class. Requires :py:meth:`get_grid`
    method to be implemented."""

    def __init__(self, med, name, cfg=None, **kwargs):
        """Build setting gridded to `True`.

        :param med: Mediator.
        :param name: Data-source name. Default is `None`.
        :param cfg: Data-source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        #: Geographic dimensions. Default values.
        self.dims = ['lat', 'lon']

        #: Mask.
        self.mask = None

        #: Stacked mask.
        self.stacked_mask = None

        #: Points in area.
        self.points_in_area = None

        #: Stacked flags for grid points in area.
        self._is_in_stack = None

        super(GriddedDataSourceBase, self).__init__(
            med, name, cfg=cfg, **kwargs)

        # Gridded dataset
        self.gridded = True

        # Add get_mask task
        self.task_mng['get_mask'] = True

    @abstractmethod
    def get_grid(self, *args, **kwargs):
        """Return data-source grid."""
        raise NotImplementedError

    def get_mask(self, **kwargs):
        """Get mask from :py:attr:`geo_src` for the given gridded data source
        and store it in :py:attr:`mask` data-source member.
        """
        # Get the mask
        if self.task_mng.get('get_mask'):
            # Make the mask
            if not self.cfg.get('no_verbose'):
                self.log.info('Making {} mask for {}'.format(
                    self.med.geo_src.name, self.name))
            kwargs_new = deepcopy(kwargs)
            kwargs_new['data_src'] = self
            self.mask = self.med.geo_src.make_mask(**kwargs_new)

            # Save the mask
            self.write_mask(**kwargs_new)

            # Update task manager
            self.task_mng['get_mask'] = False
        else:
            # Read mask
            if not self.cfg.get('no_verbose'):
                self.log.info('{} mask for {} already made'.format(
                    self.med.geo_src.name, self.name))
            self.read_mask(**kwargs)

    def get_stacked_mask(self, **kwargs):
        """Get stacked mask for area from :py:attr:`geo_src`
        for the given gridded data source and store it in
        :py:attr:`stacked_mask` data-source member.

        .. seealso:: :py:meth:_get_points_in_area
        """
        if self.stacked_mask is None:
            # Get mask
            self.get_mask(**kwargs)

            # Get points in area
            self._get_points_in_area(**kwargs)

            # Store stacked mask
            self.stacked_mask = self.mask.stack(stacked_dim=self.dims)[
                {'stacked_dim': self._is_in_stack}]

    def get_grid_postfix(self, **kwargs):
        """Return empty grid postfix string.

        returns: Grid postfix.
        rtype: str
        """
        return ''

    def get_mask_postfix(self, **kwargs):
        """Get mask postfix for data source.

        :returns: Postfix
        :rtype: str
        """
        grid_postfix = self.get_grid_postfix(**kwargs)
        geo_postfix = self.med.geo_src.get_data_postfix(**kwargs)
        postfix = '_{}{}_{}{}'.format(
            self.med.geo_src.name, geo_postfix, self.name, grid_postfix)

        return postfix

    def get_mask_path(self, makedirs=True, **kwargs):
        """Get mask file path for data source.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Filepath.
        :rtype: str
        """
        file_dir = self.med.cfg.get_project_data_directory(
            self, makedirs=makedirs, **kwargs)
        filename = 'mask{}'.format(self.get_mask_postfix(**kwargs))
        filepath = os.path.join(file_dir, filename)

        return filepath

    def read_mask(self, **kwargs):
        """Default implementation: read mask dataset as
        :py:class:`xarray.Dataset`.
        """
        filepath = '{}.nc'.format(self.get_mask_path(makedirs=False, **kwargs))
        if not self.cfg.get('no_verbose'):
            self.log.info('Reading {} mask for {} from {}'.format(
                self.med.geo_src.name, self.name, filepath))
        self.mask = xr.load_dataset(filepath)

    def write_mask(self, **kwargs):
        """Default implementation: write mask as
        :py:class:`xarray.Dataset` to netcdf.
        """
        filepath = '{}.nc'.format(self.get_mask_path(**kwargs))
        if not self.cfg.get('no_verbose'):
            self.log.info('Writing {} mask for {} to {}'.format(
                self.med.geo_src.name, self.name, filepath))
        self.mask.to_netcdf(filepath)

    def get_regional_mean(self, ds, **kwargs):
        """Average dataset over regions given by mask.

        :param ds: Dataset to average.
        :type ds: :py:class:`xarray.Dataset` of :py:class:`xarray.DataArray`

        :returns: Dataset containing regional means.
        :rtype: :py:class:`xarray.Dataset` of :py:class:`xarray.DataArray`
        """
        if not self.cfg.get('no_verbose'):
            self.log.info('Getting regional averages on {} grid'.format(
                self.name))

        if 'stacked_dim' in ds.coords:
            # Get stacked mask
            self.get_stacked_mask(**kwargs)
            mask = self.stacked_mask
        else:
            # Get mask
            self.get_mask(**kwargs)
            mask = self.mask

        # Get regional mean
        gp = ds.groupby(mask['mask'])

        # Get group means
        res = gp.mean(gp._group_dim, keep_attrs=True)

        # Remove unnecessary regions out of non-empty ones
        # and replace coordinates
        (filled_indices, idx1, idx2) = np.intersect1d(
            mask['region_index'].values, list(gp.groups),
            return_indices=True)
        res = res.loc[{'mask': filled_indices}]
        res = res.rename(mask='region')
        res['region'] = mask['region'].values[idx1]

        # Transpose region and time dimensions,
        # keeping other dimensions behind
        dim_list = list(res.dims)
        dim_list.remove('region')
        dim_list.insert(0, 'region')
        dim_list.remove('time')
        dim_list.insert(0, 'time')
        res = res.transpose(*dim_list)

        return res

    def get_total_mean(self, ds, **kwargs):
        """Average dataset over all grid points,
        independently of mask.

        :param ds: Dataset to average.
        :type ds: :py:class:`xarray.Dataset`

        :returns: Dataset containing mean.
        :rtype: :py:class:`xarray.Dataset`
        """
        if not self.cfg.get('no_verbose'):
            self.log.info('Getting {} total mean'.format(self.name))

        # Group dimensions may either original or stacked ones
        try:
            res = ds.mean(self.dims, keep_attrs=True)
        except ValueError:
            res = ds.mean(ds.stacked_dim, keep_attrs=True)

        return res

    def crop_area(self, ds, **kwargs):
        """Crop :py:obj:`ds` for data source
        over area covered by mask regions.

        :param ds: Dataset to crop.
        :type ds: :py:class:`xarray.Dataset`

        :returns: Cropped dataset.
        :rtype: :py:class:`xarray.Dataset`

        .. seealso:: :py:meth:get_stacked_mask
        """
        if not self.cfg.get('no_verbose'):
            self.log.info('Cropping area for {}'.format(self.name))

        # Make stacked mask
        self.get_stacked_mask(**kwargs)

        # Select region, removing other points
        res = ds.stack(stacked_dim=self.dims)[
            {'stacked_dim': self._is_in_stack.values}]

        return res

    def _get_points_in_area(self, **kwargs):
        """Get grid points in area."""
        if (self.points_in_area is None) or (self._is_in_stack is None):
            is_in = xr.zeros_like(self.mask['mask'], dtype=bool)
            for reg_idx in self.mask.region_index.astype(float).values:
                is_in |= (self.mask['mask'] == reg_idx)

            # Add points in area mask to regional mask dataset
            self.points_in_area = is_in

            self._is_in_stack = self.points_in_area.stack(
                stacked_dim=self.dims)


def get_geodetic_crs(cube):
    """Get geodetic Coordinate Reference System (CRS) from arbitrary system.

    :param cube: Iris cube from which to manage grids associated with
      dataset.
    :type cube: :py:class:`iris.Cube`

    :returns: Longitudes and latitudes, source CRS and geodetic CRS.
    :rtype: :py:class:`tuple` containing a :py:class:`list` and two
      CRSs.

    .. seealso:: :py:func:`get_geodetic_array`
    """
    # Get the coordinate system
    cs = cube.coord_system()

    # Get coordinates
    coords = [cube.coord('grid_longitude'), cube.coord('grid_latitude')]

    # Check if coordinate system is defined
    if cs is None:
        return coords, None, None

    # Get source CRS
    src_crs = cs.as_cartopy_crs()

    # Get geodetic CRS
    dst_crs = src_crs if src_crs.is_geodetic() else src_crs.as_geodetic()

    return coords, src_crs, dst_crs


def get_geodetic_array(ds, coords, src_crs, dst_crs):
    """ Return an array from a file making sure that geodetic longitudes
    `lon` and latitudes `lat` are included.

    :param ds: Original dataset.
    :type ds: :py:class:`xarray.Dataset`

    :returns: Geodetic array.
    :rtype: :py:class:`xarray.Dataset`

    .. seealso:: :py:func:`get_geodetic_crs`
    """
    if ('lat' not in ds.coords) or ('lon' not in ds.coords):
        # Get source grid
        x, y = coords[0].points, coords[1].points
        if x.shape != y.shape:
            x, y = np.meshgrid(x, y)

        # Convert coordinates to geodetic
        dst_coords = dst_crs.transform_points(src_crs, x, y)

        # Add the coordinates to the array
        coords_names = [c.variable_name for c in coords]
        src_coords = [(cn, ds.coords[cn]) for cn in coords_names[::-1]]
        ds.coords['lon'] = xr.DataArray(dst_coords[:, :, 0],
                                        coords=src_coords)
        ds.coords['lat'] = xr.DataArray(dst_coords[:, :, 1],
                                        coords=src_coords)

    return ds


def get_nearest_neighbor(
        ds, ref_lat, ref_lon, lat_label='lat', lon_label='lon',
        nn_tree=None, drop=False, **kwargs):
    """Evaluate dataset at point nearest to the given point.

    :param ds: Dataset to evaluate.
    :param ref_lat: Reference-point latitude.
    :param ref_lon: Reference-point longitude.
    :param lat_label: Label of latitude coordinate in dataset.
    :param lon_label: Label of longitude coordinate in dataset.
    :param nn_tree: Nearest-neighbor tree. Default is `None`,
      in which case it is computed for the dataset grid.
    :param drop: Whether to drop horizontal dimensions. Default is `False`.
    :type ds: :py:class:`xarray.Dataset` or :py:class:`xarray.DataArray`
    :type ref_lat: float
    :type ref_lon: float
    :type lat_label: str
    :type lon_label: str
    :type nn_tree: :py:class:`scipy.spatial.KDTree`
    :type drop: bool

    :returns: Selected data, neirest neighbor index and distance to reference
      point.
    :rtype: :py:class:`tuple` of :py:class:`xarray.Dataset`
      or :py:class:`xarray.DataArray`, :py:class:`int`, :py:class:`float`
    """
    if nn_tree is None:
        # Get dataset latitude and longitudes
        LAT, LON = ds[lat_label].values, ds[lon_label].values
        if len(LAT.shape) == 1:
            LAT, LON = np.meshgrid(LAT, LON)
        lat, lon = LAT.flatten(), LON.flatten()
        ds_latlon = np.array([lat, lon]).T

        # Create nearest neighbor tree
        nn_tree = cKDTree(ds_latlon)

    # Get nearest neighbor
    ref_latlon = np.array([ref_lat, ref_lon])
    nn_dist, nn_idx = nn_tree.query(ref_latlon)

    # Select data using where in case lat/lon not coordinates
    nn_latlon = ds_latlon[nn_idx]
    ds_nn = ds.where((ds[lat_label] == nn_latlon[0]) &
                     (ds[lon_label] == nn_latlon[1]), drop=True)

    # Squeeze horizontal coordinates
    ds_nn = ds_nn.squeeze(drop=drop)

    ds_nn.attrs['nearest_neighbor_index'] = nn_idx
    ds_nn.attrs['nearest_neighbor_distance'] = nn_dist

    return ds_nn
