"""CBS API for the Netherlands."""
import os
import requests
import pandas as pd
import xarray as xr
from ..data_source import DataSourceLoaderBase
from ..component import (
    DataSourceWithComponentsMixin, parse_variable_component_args,
    download_to_compute_capacity_factor, compute_capacity_factor,
    finalize_dataset)


class DataSource(DataSourceLoaderBase, DataSourceWithComponentsMixin):
    """cbs.nl data source."""
    #: Default source name.
    DEFAULT_SRC_NAME = 'cbs'

    #: Area: `'Netherlands'`
    AREA = 'Netherlands'

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
          `CBS <https://opendata.cbs.nl/statline/portal.html>`.
        """
        # Loop over variables
        for variable_name, component_names in variable_component_names.items():
            if not self.cfg.get('no_verbose'):
                self.log.info('- {}:'.format(variable_name))

            # Loop over components
            for component_name in component_names:
                # Get URL
                url = self._get_url(
                    variable_name, component_name, **kwargs)
                filepath = self._get_download_filepath(
                    variable_name, component_name, **kwargs)
                if not self.cfg.get('no_verbose'):
                    self.log.info('--- {} from {} to {}'.format(
                        component_name, url, filepath))

                # Request and raise exception if needed
                response = requests.get(url)
                response.raise_for_status()

                # Make data frame
                records = response.json()['value']
                df = pd.DataFrame(records).set_index('Perioden')
                index = ('{}-12-31'.format(t[:4]) for t in df.index)
                df.index = pd.DatetimeIndex(index)
                df.index.name = 'time'

                # Write data frame
                df.to_csv(filepath)

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
        :rtype: :py:class:`xarray.Dataset()`
        """
        # Get place names for source
        src_place_regions, _ = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, self.AREA, **kwargs))
        place_names = list(src_place_regions)

        # Loop over variables
        ds = xr.Dataset()
        for variable_name, component_names in variable_component_names.items():
            if not self.cfg.get('no_verbose'):
                self.log.info('- {}:'.format(variable_name))

            # Loop over components
            da = None
            for component_name in component_names:
                # Get filepath
                filepath = self._get_download_filepath(
                    variable_name, component_name, **kwargs)
                if not self.cfg.get('no_verbose'):
                    self.log.info('-- {} from {}'.format(
                        component_name, filepath))

                # Read data frame
                df_comp = pd.read_csv(
                    filepath, **self.cfg['read_csv_kwargs'])
                df_comp.columns = [component_name]

                # Convert to data array
                da_comp = xr.DataArray(df_comp, dims=('time', 'component'))

                # Add component to data array
                da = (da_comp if da is None else
                      xr.concat([da, da_comp], dim='component'))

            # Add area as region coordinate
            da = da.expand_dims('region').assign_coords(
                region=place_names)

            # Add variable to dataset
            ds[variable_name] = da

        return ds

    def _get_capacity_factor(self, ds, **kwargs):
        """Get capacity factor from generation and capacity.

        :param ds: Dataset containing generation and capacity.
        :type ds: mapping

        :returns: Capacity factor.
        :rtype: :py:class:`xarray.DataArray`
        """
        da_gen = ds['generation']

        # Get number of days in month
        time = da_gen.indexes['time']
        start = pd.Timestamp(time[0])
        end = pd.Timestamp(time[-1]) + pd.Timedelta('366 days')
        time_plus = pd.date_range(start=start, end=end, freq='Y')
        ndays = (time_plus[1:] - time_plus[:-1]).days
        da_ndays = xr.DataArray(ndays, coords=[('time', time)])
        da_nhours = da_ndays * 24

        # Get capacity factor
        da = da_gen / (ds['capacity'] * da_nhours)

        return da

    def _get_url(self, variable_name, component_name, **kwargs):
        """Get URL for query.

        :param variable_name: Name of variable to query.
        :param component_name: Name of component to query.
        :type variable_name: str
        :type component_name: str

        :returns: URL.
        :rtype: str
        """
        # Filter component
        filter_component = "BronTechniek eq '{}'".format(
            self.cfg['component_keys'][component_name])

        # Filter periods
        filter_time = ("substring(Perioden, 0, 4) ge '{}' and "
                       "substring(Perioden, 0, 4) le '{}'"
                       "substring(Key,4,2) eq 'JJ'".format(
                           self.cfg['first_year'], self.cfg['last_year']))

        # Compile filters
        filters = '{} and {}'.format(filter_component, filter_time)

        # Select properties
        select = 'Perioden,{}'.format(
            self.cfg['variable_names'][variable_name])

        # Define URL
        url = '{}/{}/{}?$filter={}&$select={}'.format(
            self.cfg['host'], self.cfg['variable_identifiers'][variable_name],
            self.cfg['data_entity'], filters, select)

        return url

    def _get_download_filepath(self, variable_name, component_name, **kwargs):
        """Get download filepath.

        :param variable_name: Name of variable to query.
        :param component_name: Name of component to query.
        :type variable_name: str
        :type component_name: str

        :returns: Filepath.
        :rtype: str
        """
        # Define filename
        filename = '{}_{}_{}{}.csv'.format(
            self.name, variable_name, component_name, self.get_postfix())

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
