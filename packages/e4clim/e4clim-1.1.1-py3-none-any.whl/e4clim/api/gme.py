"""GME API."""
import os
import requests
import zipfile
from io import BytesIO
import pandas as pd
import xarray as xr
from ..container import ensure_collection
from ..data_source import DataSourceLoaderBase
from ..component import (DataSourceWithComponentsMixin,
                         parse_variable_component_args,
                         finalize_dataset)


COMPONENT_NAME = 'demand'
VARIABLE_NAME = 'demand'


class DataSource(DataSourceLoaderBase, DataSourceWithComponentsMixin):
    #: Default source name.
    DEFAULT_SRC_NAME = 'gme'

    #: Area: `'Italy'`.
    AREA = 'Italy'

    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping

        .. note:: The GME data is downloaded from the
          `GME website <http://www.gestoremercatienergetici.org>`_.
        """
        name = name or self.DEFAULT_SRC_NAME
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def download(self, **kwargs):
        """Download GME data source.

        :param variable_component_names: Names of components to download per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to :py:class:`set` of :py:class:`str`

        :returns: Names of downloaded components per variable.
        :rtype: mapping from :py:class:`str` to :py:class:`set` of
          :py:class:`str`
        """
        years = range(int(self.cfg['first_year']),
                      int(self.cfg['last_year']) + 1)
        for year in years:
            # Download file
            url = self._get_url(year, **kwargs)
            if not self.cfg.get('no_verbose'):
                self.log.info('- Year {} from {}'.format(year, url))

            # Request and raise exception if needed
            response = requests.get(url)
            response.raise_for_status()

            # Get zip
            zip_ref = zipfile.ZipFile(BytesIO(response.content))

            # Get filepath with extension
            filepath = self._get_download_filepath(year, **kwargs)
            extension = os.path.splitext(zip_ref.filelist[0].filename)[-1]
            filepath = '{}{}'.format(filepath, extension)

            # Unzip single file
            zip_ref.filelist[0].filename = os.path.basename(filepath)
            zip_ref.extract(zip_ref.filelist[0], os.path.dirname(filepath))
            zip_ref.close()

        # Return names of downloaded variables
        return {VARIABLE_NAME: {COMPONENT_NAME}}

    @parse_variable_component_args
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
        # Check if demand in variable and component names
        if set(variable_component_names) != (
                ensure_collection(VARIABLE_NAME, set)):
            raise ValueError("Variable names different from {'{}'}".format(
                VARIABLE_NAME))

        if variable_component_names[VARIABLE_NAME] != (
                ensure_collection(COMPONENT_NAME, set)):
            raise ValueError("Component names different from {'{}'}".format(
                COMPONENT_NAME))

        # Get places and regions
        src_place_regions, _ = self.med.geo_src.get_place_regions_for_source(
            self.name, self.AREA, **kwargs)

        # Read demand from file
        years = range(int(self.cfg['first_year']),
                      int(self.cfg['last_year']) + 1)
        da = None
        for year in years:
            # Read downloaded file
            df = self._read_downloaded_file(year, **kwargs)

            # Set UTC datetime index from 'Europe/Rome' time with DST
            start = pd.to_datetime(
                str(df.iloc[0, 0]) + '{:02d}'.format(df.iloc[0, 1] - 1),
                format='%Y%d%m%H')
            df.index = pd.date_range(
                start=start, freq='H', periods=df.shape[0],
                tz='Europe/Rome').tz_convert(None)

            # Groupby zones, summing energy
            df_zones = pd.DataFrame(
                0., index=df.index, columns=list(src_place_regions))
            for place_name, region_names in src_place_regions.items():
                df_zones[place_name] = df[region_names].sum('columns')

            # Select zones and convert to DataArray
            da_year = xr.DataArray(df_zones, dims=('time', 'region'))

            # Add array to record
            da = (da_year if da is None else
                  xr.concat([da, da_year], dim='time'))

        # Remove the years appearing from conversion to UTC
        first_date = '{}-01-01'.format(years[0])
        last_date = '{}-12-31'.format(years[-1])
        da = da.sel(time=slice(first_date, last_date))
        da['time'].attrs['timezone'] = 'UTC'

        # Add component dimension
        da = da.expand_dims('component').assign_coords(
            component=[COMPONENT_NAME])

        # Add demand to dataset
        ds = {VARIABLE_NAME: da}

        return ds

    def _read_downloaded_file(self, year, **kwargs):
        """Read downloaded file.

        :param year: Year for which to read file.
        :type year: int

        :returns: Data frame read from file.
        :rtype: :py:class:`pandas.DataFrame`
        """
        # Get filepath
        filepath = self._get_download_filepath(year, **kwargs)

        # Read file as xls or xlsx
        if not self.cfg.get('no_verbose'):
            self.log.info('- Year {} from {}'.format(
                year, filepath))
        try:
            filepath_ext = filepath + '.xls'
            df = pd.read_excel(filepath_ext, sheet_name=self.cfg['sheet_name'])
        except FileNotFoundError:
            filepath_ext = filepath + '.xlsx'
            df = pd.read_excel(filepath_ext, sheet_name=self.cfg['sheet_name'])

        return df

    def _get_url(self, year, **kwargs):
        """Get url.

        :param year: Year.
        :type year: int

        :returns: Filepath.
        :rtype: str

        .. note:: Dates in filepath are in UTC.
        """
        zip_filename = 'Anno{}.zip'.format(year)
        url = os.path.join(self.cfg['host'], zip_filename)

        return url

    def _get_download_filepath(self, year, **kwargs):
        """Get download filepath without extension.

        :param year: Year.
        :type year: int

        :returns: Filepath.
        :rtype: str

        .. note:: Dates in filepath are in UTC.
        """
        # Define filename
        filename = '{}_{}_{}'.format(
            self.DEFAULT_SRC_NAME, VARIABLE_NAME, year)

        # Get filepath
        src_dir = self.med.cfg.get_external_data_directory(self)
        filepath = os.path.join(src_dir, filename)

        return filepath

    def get_postfix(self, **kwargs):
        """Get postfix for GSE data source.

        returns: Postfix.
        rtype: str
        """
        postfix = '_{}-{}'.format(self.cfg['first_year'],
                                  self.cfg['last_year'])

        return postfix
