"""MERRA-2 API."""
import os
from collections import OrderedDict
import requests
import netCDF4 as nc
import numpy as np
import pandas as pd
import xarray as xr
from ..grid import GriddedDataSourceBase
from ..container import ensure_collection


class DataSource(GriddedDataSourceBase):
    #: Default source name.
    DEFAULT_SRC_NAME = 'merra2'

    #: Frequency code.
    FREQ_CODES = {'hour': '1', 'day': 'D', 'month': 'M'}

    #: File sampling.
    FILE_SAMPLING = {'hour': 'D', 'day': 'D', 'month': 'M'}

    #: Frequency-dependent directory.
    DIR_FREQ = {'hour': '', 'day': '', 'month': '_MONTHLY'}

    #: Time-description code.
    TIME_DESCRIPTION_CODES = {
        'cnst': 'C', 'inst': 'I', 'stat': 'S', 'tavg': 'T'}

    #: Default maximum fetch-trials.
    DEFAULT_MAX_FETCH_TRIALS = 50

    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

        # If lat_range and lon_range are not given, they will
        # be computed from mask regions total bounds when needed
        self.lat_range = self.cfg.get('lat_range')
        self.lon_range = self.cfg.get('lon_range')

        # Time range
        self.time_range = self.cfg.get('time_range')
        if self.time_range is None:
            if ((self.cfg['time_description'] == 'stat')
                    or (self.cfg['frequency'] == 'month')):
                # Only one sample per day
                self.time_range_str = '[0:0]'
            elif self.cfg['time_description'] == 'tavg':
                # Default: get 24 hours of day
                self.time_range_str = '[0:23]'
        else:
            # User-defined time range
            self.time_range_str = '[{}:{}]'.format(
                self.time_range[0], self.time_range[1])

        # Server parent directory
        host_dir = (self.DEFAULT_SRC_NAME.upper()
                    + self.DIR_FREQ[self.cfg['frequency']])
        self.srv_parent_dir = '{}/opendap/hyrax/{}/{}{}{}{}{}'.format(
            self.cfg['host'], host_dir, self.cfg['data_name'],
            self.TIME_DESCRIPTION_CODES[self.cfg['time_description']],
            self.FREQ_CODES[self.cfg['frequency']],
            self.cfg['horizontal_resolution'],
            self.cfg['vertical_location'].upper())

        # Maximum fetch trials
        self.max_fetch_trials = (self.cfg.get('max_fetch_trials') or
                                 self.DEFAULT_MAX_FETCH_TRIALS)

    def download(self, variable_names=None, **kwargs):
        """Download merra2 data and save it to disk.

        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr:`variable_names` are downloaded.
        :type variable_names: (collection of) :py:class:`str`

        :returns: Names of downloaded variables.
        :rtype: :py:class:`set` of :py:class:`str`
        """
        # Get variable names
        variable_names = ensure_collection(
            variable_names, set) or self.variable_names

        # Loop over days
        date_range = pd.date_range(
            start=self.cfg['start_date'], end=self.cfg['end_date'],
            freq=self.FILE_SAMPLING[self.cfg['frequency']], closed='left')
        for date in date_range:
            for variable_name in variable_names:
                # Download data for date and variable
                self._download_date_variable(
                    date, variable_name, download=True, **kwargs)

        return variable_names

    def load(self, transform=None, variable_names=None, **kwargs):
        """Collect all required variables from the MERRA-2 re-analysis.

        :param transform: A function or a composee of functions
          to apply to the datasets.
          These functions should take as arguments a dataset and a
          :py:class:`.data_source.DataSourceBase` data source.
        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr:`variable_names` are downloaded.
        :type transform: :py:class:`func` or
          :py:class:`.data_source.Composer`
        :type variable_names: (collection of) :py:class:`str`

        :returns: A dataset collecting all variables and periods.
        :rtype: :py:class:`xarray.Dataset`
        """
        # Get variable names
        variable_names = ensure_collection(
            variable_names, set) or self.variable_names

        # Loop over days
        date_range = pd.date_range(
            start=self.cfg['start_date'], end=self.cfg['end_date'],
            freq=self.FILE_SAMPLING[self.cfg['frequency']], closed='left')
        ds = None
        for date in date_range:
            # Collect all variables from all groups
            ds_per = xr.Dataset()
            if not self.cfg.get('no_verbose'):
                self.log.info('Reading data for {}'.format(
                    date.date()))
            for variable_name in variable_names:
                src_variable_name = self.cfg['variable_names'].get(
                    variable_name)

                # Read data for date and variable
                ds_gp = self._download_date_variable(
                    date, variable_name, download=False, **kwargs)
                if ds_gp is None:
                    continue

                # Add height
                self._add_height(ds_gp)

                # Rename variable
                ds_gp = ds_gp.rename(**{src_variable_name: variable_name})

                # Merge group
                ds_per = ds_per.merge(ds_gp)
                ds_gp.close()

            # Remove conflicting attributes to avoid
            # AttributeError: NetCDF: String match to name in use
            try:
                del ds_per.time.attrs['CLASS']
                del ds_per.time.attrs['NAME']
            except KeyError:
                pass

            # Apply functions to the dataset if given
            if transform:
                kwargs.update({'ds': ds_per, 'data_src': self})
                ds_per = transform(**kwargs)

            # Create or add period
            ds = ds_per if ds is None else xr.concat([ds, ds_per], dim='time')

        # Change hour interval representation convention from center to left
        t = ds.indexes['time']
        index_parts = {'year': t.year, 'month': t.month, 'day': t.day}
        if self.cfg['frequency'] == 'hour':
            index_parts['hour'] = t.hour
        new_index = pd.to_datetime(index_parts)
        ds = ds.reindex(time=new_index, method='bfill')
        ds.time.encoding['units'] = "hours since 1980-01-01T00:00:00"

        return ds

    def get_postfix(self, start_date=None, end_date=None, **kwargs):
        """Get postfix for the MERRA-2 data.

        :param start_date: Simulation start-date. Default is `None`, in which
          case the first date of `self.cfg['streams']['start_dates']` is used.
        :param end_date: Simulation end-date. Default is `None`, in which case
          the first date of `self.cfg['streams']['end_dates']` is used.
        :type start_date: str
        :type end_date: str

        :returns: Postfix.
        :rtype: str
        """
        start_date = start_date or self.cfg['start_date']
        end_date = end_date or self.cfg['end_date']

        # Get paths
        postfix = '_{}_{}-{}'.format(self.cfg['frequency'],
                                     start_date, end_date)

        return postfix

    def get_index_lon(self, lon):
        """Get grid index corresponding to longitude.

        :param lon: Longitude.
        :type lon: :py:class:`float`, array_like

        :returns: Longitude grid-index.
        :rtype: :py:class:`int`, :py:class:`numpy.array`
        """
        ilon = (lon + 180.) / self.cfg['delta_lon']
        try:
            ilon = int(ilon + 0.1)
        except TypeError:
            ilon = (np.array(ilon) + 0.1).astype(int)

        return ilon

    def get_index_lat(self, lat):
        """Get grid index corresponding to latitude.

        :param lat: Latitude.
        :type lat: :py:class:`float`, array_like

        :returns: Latitude grid-index.
        :rtype: :py:class:`int`, :py:class:`numpy.array`
        """
        ilat = (lat + 90.) / self.cfg['delta_lat']
        try:
            ilat = int(ilat + 0.1)
        except TypeError:
            ilat = (np.array(ilat) + 0.1).astype(int)

        return ilat

    def get_lat_lon_range_from_geo_bounds(self):
        """Get latitude and longitude ranges from bounds of geographic
        data source."""
        # Get total bounds in geoid system
        lon_min, lat_min, lon_max, lat_max = (
            self.med.geo_src.get_total_bounds(epsg=4326))

        # Set ranges
        self.lat_range = [lat_min, lat_max]
        self.lon_range = [lon_min, lon_max]

    def get_lat_lon_range_str(self):
        """Convert lat/lon range to indices string."""
        lat_min = self.lat_range[0]
        lat_max = self.lat_range[1]
        lon_min = self.lon_range[0]
        lon_max = self.lon_range[1]

        # Convert bounds to grid indices
        ilon_min = self.get_index_lon(lon_min)
        ilon_max = self.get_index_lon(lon_max) + 1
        ilat_min = self.get_index_lat(lat_min)
        ilat_max = self.get_index_lat(lat_max) + 1

        # Get grid string
        self.lon_range_str = '[{:d}:{:d}]'.format(ilon_min, ilon_max)
        self.lat_range_str = '[{:d}:{:d}]'.format(ilat_min, ilat_max)

    def get_url_file_dir_file(self, variable_name=None, date=None):
        """Get variable URL, directory and filename for MERRA-2 data.

        :param variable_name: Variable name. Default is `None`.
        :param date: Date for which to return paths.
          If `None`, use `'start_date'` value of data-source configuration.
          Default is `None`.
        :type variable_name: str

        returns: Source URL, directory and filename.
        :rtype: :py:class:`tuple` of :py:class:`str`
        """
        if (not self.lat_range) or (not self.lon_range):
            # Get lat/lon range from bounds of geographic data
            self.get_lat_lon_range_from_geo_bounds()

        # Convert lat/lon range to indices string
        self.get_lat_lon_range_str()

        # Define grid string
        domain = '{}{}{}'.format(self.time_range_str, self.lat_range_str,
                                 self.lon_range_str)
        short_time_range_str = ('' if self.cfg['space'] == '2d'
                                else self.time_range_str)
        grid_list = 'time{},lat{},lon{}'.format(
            short_time_range_str, self.lat_range_str, self.lon_range_str)

        # Get data-source directory
        src_dir = self.med.cfg.get_external_data_directory(self)

        # Get given date or start date
        date = pd.Timestamp(date or self.cfg['start_date'])

        # Get runid of stream containg date
        for (stream, cfg_stream) in self.cfg['streams'].items():
            ssd = pd.Timestamp(cfg_stream['start_date'])
            sed = pd.Timestamp(cfg_stream['end_date'])
            if (date >= ssd) & (date < sed):
                break
        runid = '{}{}'.format(stream, self.cfg['version'])
        freq = '{}{}'.format(self.cfg['time_description'],
                             self.FREQ_CODES[self.cfg['frequency']])
        prefix0 = '{}_{}.{}_{}'.format(
            self.DEFAULT_SRC_NAME.upper(), runid, freq, self.cfg['space'])

        if variable_name is None:
            # Take first variable in a group
            group_name = None
            it = 0
            while group_name is None:
                variable_name = list(self.variable_names)[it]
                group_name = self.cfg['group_names'].get(variable_name)
                it += 1
        else:
            # Try to get group of variable
            group_name = self.cfg['group_names'].get(variable_name)
        src_variable_name = self.cfg['variable_names'].get(variable_name)

        # Make local directories
        file_dir = os.path.join(src_dir, group_name)
        os.makedirs(file_dir, exist_ok=True)

        # Frequency dependent variables
        date_dir = '{:04d}'.format(date.year)
        if self.cfg['frequency'] in ['hour', 'day']:
            date_dir += '/{:02d}'.format(date.month)
            date_file = date.strftime('%Y%m%d')
        else:
            date_file = date.strftime('%Y%m')

        HV = '{}{}'.format(self.cfg['horizontal_resolution'],
                           self.cfg['vertical_location'])
        prefix = '{}_{}_{}.{}.{}'.format(
            prefix0, group_name, HV, date_file, self.cfg['format'])
        postfix = '{}{},{}'.format(src_variable_name, domain, grid_list)
        filename = '{}.nc?{}'.format(prefix, postfix)

        srv_dir = '{}{}.{}'.format(
            self.srv_parent_dir, group_name.upper(), self.cfg['geos5_version'])
        url = '{}/{}/{}'.format(srv_dir, date_dir, filename)

        return url, file_dir, filename

    def get_grid(self, *args, **kwargs):
        """Get grid used to make masks.

        :returns: Dataset coordinates.
        :rtype: :py:class:`tuple` of pairs of :py:class:`str`
          and :py:class:`numpy.array`
        """
        # Get paths
        url, file_dir, filename = self.get_url_file_dir_file()

        # Read coords
        filepath = os.path.join(file_dir, filename)
        if not self.cfg.get('no_verbose'):
            self.log.info('Reading coordinates from {}'.format(filepath))
        with xr.open_dataset(filepath) as ds:
            coords = OrderedDict({
                'lat': ds['lat'].copy(deep=True).values,
                'lon': ds['lon'].copy(deep=True).values})

        return coords

    def get_grid_postfix(self, *args, **kwargs):
        """Grid postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}{}'.format(self.cfg['horizontal_resolution'],
                                 self.cfg['vertical_location'])

        return postfix

    def _download_request(self, url):
        """Download data over HTTP - OPeNDAP.

        :param url: OPeNDAP URL.
        :type url: str

        :returns: Dataset.
        :rtype: :py:class:`xarray.Dataset`
        """
        # Request and raise exception if needed
        response = requests.get(url)
        response.raise_for_status()

        # Convert bytes to netCDF4.Dataset
        ds_nc = nc.Dataset(filename='dum.nc', memory=response.content)

        # Convert netCDF4.Dataset to xarray.Dataset
        ds = xr.open_dataset(xr.backends.NetCDF4DataStore(ds_nc))

        return ds

    def _download_date_variable(
            self, date, variable_name, download=False, **kwargs):
        """Download data for given date and variable.

        :param date: Date.
        :param variable_name: Variable name.
        :param download: Whether to direclty download data, or to try to
          read it from disk first. Default is `False`, in which case
          an attempt is made to read first.
        :type date: datetime
        :type variable_name: str
        :type download: bool
        """
        # Get group name for variable
        group_name = self.cfg['group_names'].get(variable_name)
        src_variable_name = self.cfg['variable_names'].get(variable_name)
        if (src_variable_name is None) or (group_name is None):
            self.log.warning(
                "{} variable not in 'variable_names' of {} "
                "configuration-file: skipping".format(
                    variable_name, self.name))
            return

        # Get paths
        url, file_dir, filename = self.get_url_file_dir_file(
            variable_name=variable_name, date=date)

        # Fetch data
        n_trials = 0
        while n_trials < self.max_fetch_trials:
            try:
                if (not download) and (n_trials == 0):
                    # Read previously downloaded data
                    filepath = os.path.join(file_dir, filename)
                    ds = xr.open_dataset(filepath)
                else:
                    # Try to fetch
                    if not self.cfg.get('no_verbose'):
                        self.log.info('Fetching {} group from {}'.format(
                            group_name, url))
                    ds = self._download_request(url)

                # Check quality
                if self.cfg.get('check_quality'):
                    _quality_check(ds)

                # Everything went well -> leave trials loop
                break
            except (OSError, RuntimeError,
                    AttributeError, ValueError) as e:
                # Retry
                self.log.warning(
                    'Fetching trial {:d} failed: {}'.format(
                        n_trials + 1, str(e)))
                n_trials += 1
                continue

        # Verify that last trial succeeded
        if n_trials >= self.max_fetch_trials:
            # All trials failed
            self.log.critical('Fetching failed after {:d} '
                              'trials.'.format(n_trials))
            raise RuntimeError
        elif download or (n_trials > 0):
            # Write data
            filepath = os.path.join(file_dir, filename)
            if not self.cfg.get('no_verbose'):
                self.log.info('Writing {} group to {}'.format(
                    group_name, filepath))
            ds.to_netcdf(filepath)

        return ds

    def _add_height(self, ds):
        """Add or rename `'height'` variable to dataset attributes.

        :param ds: Dataset.
        :type ds: :py:class:`xarray.Dataset`
        """
        for svn in ds.data_vars:
            var = ds[svn]
            if self.cfg['height'] not in var.attrs:
                # Add height as attribute
                if self.cfg['height'] in ds:
                    var.attrs['height'] = float(
                        ds[self.cfg['height']])
                elif self.cfg['height'] in ds.coords:
                    var.attrs['height'] = float(
                        ds.coords[self.cfg['height']])
                else:
                    # Get height from wind name or assume 2m height
                    var.attrs['height'] = (
                        float(svn[1:svn.find('M')])
                        if svn[0] in ['U', 'V'] else 2.)
            else:
                # Rename
                var.attrs['height'] = var.attrs[self.cfg['height']]


def _quality_check(ds):
    """Check integrity of downloaded dataset. If dataset is invalid,
    `ValueError` is raised.

    :param ds: Dataset to check.
    :type ds: :py:class:`xarray.Dataset`
    """
    # Time index
    if (ds.indexes['time'].year == 1970).any():
        raise ValueError

    # NaN and Infinite values
    for da in ds.values():
        if da.isnull().any() or (da > 1e10).any():
            raise ValueError
