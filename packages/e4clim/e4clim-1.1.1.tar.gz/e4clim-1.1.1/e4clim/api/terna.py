"""Terna API for Italy."""
import os
import requests
import numpy as np
import pandas as pd
import xarray as xr
from ..data_source import DataSourceLoaderBase
from ..component import (
    DataSourceWithComponentsMixin, parse_variable_component_args,
    download_to_compute_capacity_factor, compute_capacity_factor,
    finalize_dataset)


class DataSource(DataSourceLoaderBase, DataSourceWithComponentsMixin):
    """terna.it data source."""
    #: Default source name.
    DEFAULT_SRC_NAME = 'terna'

    #: Area: `'Italy'`
    AREA = 'Italy'

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

    @parse_variable_component_args
    @download_to_compute_capacity_factor
    def download(self, variable_component_names, **kwargs):
        """Download data.

        :param variable_component_names: Names of components to download per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to :py:class:`set` of :py:class:`str`

        :returns: Names of downloaded components per variable.
        :rtype: mapping from :py:class:`str` to :py:class:`set` of
          :py:class:`str`

        .. note:: The data is downloaded from
          `Terna <https://www.terna.it/Portals/0/Resources/visualagency/data/evoluzione_mercato_elettrico/regioni/>`.
        """
        # Get region names
        _, src_region_place = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))

        # Loop over variables
        for variable_name in variable_component_names:
            if not self.cfg.get('no_verbose'):
                self.log.info('- {}:'.format(variable_name))

            # Loop over components
            for region_name in src_region_place:
                # Get URL
                url = self._get_url(variable_name, region_name, **kwargs)
                filepath = self._get_download_filepath(
                    variable_name, region_name, **kwargs)
                if not self.cfg.get('no_verbose'):
                    self.log.info('-- {} from {} to {}'.format(
                        region_name, url, filepath))

                # Request and raise exception if needed
                response = requests.get(url)
                response.raise_for_status()

                # Write file
                with open(filepath, 'wb') as f:
                    for chunk in response:
                        f.write(chunk)

        # Return names of downloaded variables
        return variable_component_names

    @parse_variable_component_args
    @compute_capacity_factor
    @finalize_dataset
    def load(self, variable_component_names, **kwargs):
        """Load data.

        :param variable_component_names: Names of components to load per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: dict
        """
        # Get region-place mapping
        src_place_region, src_region_place = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))

        # Loop over variables
        ds = {}
        for variable_name, component_names in variable_component_names.items():
            if not self.cfg.get('no_verbose'):
                self.log.info('- {}:'.format(variable_name))

            # Manage wind component as onshore only
            component_name_requested = 'wind'
            component_to_load_names = component_names.copy()
            if component_name_requested in component_names:
                # Make sure that generation and capacity are loaded
                component_to_load_names.add('wind-onshore')

                # Remove capacity factor from components to load
                component_to_load_names.discard(component_name_requested)

            # Get source-destination component names mapping
            component_names_inv = {
                self.cfg['component_names'][component_name]:
                component_name
                for component_name in component_to_load_names}

            # Loop over regions
            da = None
            for region_name, place_name in src_region_place.items():
                # Get filepath
                filepath = self._get_download_filepath(
                    variable_name, region_name, **kwargs)
                if not self.cfg.get('no_verbose'):
                    self.log.info('-- {} from {}'.format(
                        region_name, filepath))

                # Read data frame
                df_region = pd.read_excel(
                    filepath,
                    sheet_name=self.cfg['sheet_names'][variable_name],
                    **self.cfg['read_excel_kwargs'][variable_name])

                # Select rows, if needed
                sel_row_var = self.cfg['select_rows'].get(variable_name)
                if sel_row_var:
                    for col, value in sel_row_var.items():
                        df_region = df_region.where(
                            df_region[col] == value).dropna(
                                axis='rows', how='all')

                # Correct typo in case needed
                df_region = df_region.rename(columns={
                    'fotovotaica': 'fotovoltaica'})

                # Rename components and select them
                df_region = df_region.rename(columns=component_names_inv)[
                    component_to_load_names]

                # Define time index
                df_region.index = pd.DatetimeIndex(
                    ['{}-12-31'.format(t) for t in df_region.index],
                    freq='A-DEC')
                df_region.index.name = 'time'

                # Select period
                time_slice = slice(
                    str(self.cfg['first_year']), str(self.cfg['last_year']))
                df_region = df_region.loc[time_slice]

                # Convert to data array
                da_region = xr.DataArray(
                    df_region, dims=('time', 'component')).astype(float)

                # Initialize array
                if da is None:
                    shape = da_region.shape + (len(src_place_region),)
                    coords = [da_region['time'], da_region['component'],
                              ('region', list(src_place_region))]
                    da = xr.DataArray(np.zeros(shape), coords=coords)

                # Add region data to place
                # keeping only NaNs present in all regions
                loc = {'region': place_name}
                da.loc[loc] = da_region.where(
                    da.loc[loc].isnull(),
                    da.loc[loc] + da_region.where(~da_region.isnull(), 0.))

            # Add variable to dataset
            ds[variable_name] = da

            # Make sure that generation and capacity NaNs match
            if ('generation' in ds) and ('capacity' in ds):
                isvalid_all = (~ds['generation'].isnull() &
                               ~ds['capacity'].isnull())
                ds['generation'] = ds['generation'].where(isvalid_all)
                ds['generation'] = ds['generation'].where(isvalid_all)

        return ds

    def _get_capacity_factor(self, ds, **kwargs):
        """Get capacity factor from generation and capacity.

        :param ds: Dataset containing generation and capacity.
        :type ds: mapping

        :returns: Capacity factor.
        :rtype: :py:class:`xarray.DataArray`
        """
        da_gen = ds['generation']
        da_cap = ds['capacity']

        # Interpolate capacity
        da_cap_int = da_cap.copy()
        da_cap_int[{'time': slice(1, len(da_cap.time))}] = (
            da_cap_int[{'time': slice(1, len(da_cap.time))}].values
            + da_cap_int[{'time': slice(0, -1)}].values) / 2

        # Get number of days in month
        time = da_gen.indexes['time']
        start = pd.Timestamp(time[0])
        end = pd.Timestamp(time[-1]) + pd.Timedelta('366 days')
        time_plus = pd.date_range(start=start, end=end, freq='Y')
        ndays = (time_plus[1:] - time_plus[:-1]).days
        da_ndays = xr.DataArray(ndays, coords=[('time', time)])
        da_nhours = da_ndays * 24

        # Get capacity factor
        da = da_gen / (da_cap_int * da_nhours)

        return da

    def _get_url(self, variable_name, region_name, **kwargs):
        """Get URL for query.

        :param variable_name: Name of variable to query.
        :param region_name: Region name.
        :type variable_name: str
        :type region_name: str

        :returns: URL.
        :rtype: str
        """
        filepath = self._get_download_filepath(
            variable_name, region_name, **kwargs)
        filename = os.path.basename(filepath)
        url = '{}/{}'.format(self.cfg['host'], filename)

        return url

    def _get_download_filepath(self, variable_name, region_name, **kwargs):
        """Get download filepath.

        :param variable_name: Name of variable to query.
        :param region_name: Region name.
        :type variable_name: str
        :type region_name: str

        :returns: Filepath.
        :rtype: str
        """
        # Get filename
        src_variable_name = self.cfg['variable_names'][variable_name]
        filename = '{}_{}.{}'.format(region_name, src_variable_name,
                                     self.cfg['file_format'])

        # Get filepath
        src_dir = self.med.cfg.get_external_data_directory(self)
        filepath = os.path.join(src_dir, filename)

        return filepath

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(self.cfg['first_year'],
                                  self.cfg['last_year'])

        return postfix
