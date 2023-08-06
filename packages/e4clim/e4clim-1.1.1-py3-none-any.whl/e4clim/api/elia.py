"""ELIA (BE) API."""
import os
from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
import xarray as xr
from ..data_source import DataSourceLoaderBase
from ..component import (DataSourceWithComponentsMixin,
                         parse_variable_component_args,
                         finalize_dataset)


class DataSource(DataSourceLoaderBase, DataSourceWithComponentsMixin):
    #: Default source name.
    DEFAULT_SRC_NAME = 'elia'

    #: Area: `'Belgium'`.
    AREA = 'Belgium'

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

        #: Maximum fetch trials
        self.max_fetch_trials = (self.cfg.get('max_fetch_trials') or
                                 self.DEFAULT_MAX_FETCH_TRIALS)

        #: Requests session
        self._session = None

    @parse_variable_component_args
    def download(self, variable_component_names, **kwargs):
        """Download data.

        :param variable_component_names: Names of components to download per
          variable.
        :type variable_component_names: mapping from :py:class:`str`
          to :py:class:`set` of :py:class:`str`

        :returns: Names of downloaded components per variable.
        :rtype: mapping from :py:class:`str` to :py:class:`set` of
          :py:class:`str`

        .. note:: The data is downloaded from the
          `elia's REST API <https://publications.elia.be/Publications/Publications/>`.
        """
        # Start session
        self._session = Session()

        # Get region names
        _, src_region_place = self.med.geo_src.get_place_regions_for_source(
            self.name, self.AREA, **kwargs)

        # Get dates
        date_fmt = '%Y-%m-%d'
        dates = self._get_dates(**kwargs)

        # Define start and end dates
        svar = ', '.join(str(variable_name)
                         for variable_name in variable_component_names)
        if not self.cfg.get('no_verbose'):
            self.log.info('{} variables:'.format(svar))

        # Get region IDs
        region_ids = self._get_region_ids(**kwargs)

        # Loop over variables
        for variable_name, component_names in variable_component_names.items():
            src_variable_name = self.cfg['variable_names'][variable_name]
            if not self.cfg.get('no_verbose'):
                self.log.info('- {}:'.format(variable_name))

            # Loop over components
            for component_name in component_names:
                if not self.cfg.get('no_verbose'):
                    self.log.info('-- {}:'.format(component_name))

                for d, date in enumerate(dates[:-1]):
                    date_from = date.strftime(date_fmt)
                    date_to = dates[d + 1].strftime(date_fmt)
                    if not self.cfg.get('no_verbose'):
                        self.log.info('--- from {} to {}'.format(
                            date_from, date_to))

                    # Download all regions
                    for region_name, place_name in src_region_place.items():
                        source_id = region_ids[region_name]
                        if not self.cfg.get('no_verbose'):
                            self.log.info('---- {}'.format(region_name))

                        # Get items from REST API with BeautifulSoup
                        items = self._download_request(
                            component_name, date_from, date_to, source_id,
                            **kwargs)

                        if len(items) > 0:
                            # Define time index removing UTC timezone
                            time_list = items.find_all('DateTime')
                            time = pd.DatetimeIndex(
                                (v.text for v in time_list))
                            time.name = 'time'
                            time = time.tz_convert(None)

                            # Get series
                            cf_list = items.find_all(src_variable_name)
                            fact = self.cfg['unit_conversions'][
                                component_name][variable_name]
                            s = pd.Series(
                                (float(v.text) * fact if v.text else None
                                 for v in cf_list), index=time)
                        else:
                            s = pd.DataFrame()

                        # Save locally
                        filepath = self._get_download_filepath(
                            variable_name, component_name, region_name,
                            date_from, date_to, **kwargs)
                        s.to_csv(filepath)

        # Return names of downloaded variables
        return variable_component_names

    @parse_variable_component_args
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
        # Get region names
        _, src_region_place = self.med.geo_src.get_place_regions_for_source(
            self.name, self.AREA, **kwargs)

        # Get dates
        dates = self._get_dates(**kwargs)
        date_fmt = '%Y-%m-%d'
        start = pd.Timestamp(self.cfg['start_date'], tz='utc')
        end = pd.Timestamp(self.cfg['end_date'], tz='utc')

        # Loop over datasets
        ds = {}
        for variable_name, component_names in variable_component_names.items():
            if not self.cfg.get('no_verbose'):
                self.log.info('- {}:'.format(variable_name))
            # Loop over components
            da = None
            for component_name in component_names:
                if not self.cfg.get('no_verbose'):
                    self.log.info('-- {}:'.format(component_name))

                df = pd.DataFrame()
                for d, date in enumerate(dates[:-1]):
                    date_from = date.strftime(date_fmt)
                    date_to = dates[d + 1].strftime(date_fmt)
                    if not self.cfg.get('no_verbose'):
                        self.log.info('--- from {} to {}'.format(
                            date_from, date_to))

                    df_date = pd.DataFrame(columns=src_region_place.values(),
                                           dtype=float)
                    for region_name, place_name in src_region_place.items():
                        # Read downloaded data
                        filepath = self._get_download_filepath(
                            variable_name, component_name, region_name,
                            date_from, date_to, **kwargs)
                        s = pd.read_csv(
                            filepath, index_col=0, parse_dates=True).iloc[:, 0]

                        # Add region data to place
                        if df_date[place_name].any():
                            df_date[place_name] += s
                        else:
                            df_date[place_name] = s

                    # Select regions
                    df_date = df_date[src_region_place]

                    # Concatenate dates
                    df = pd.concat([df, df_date], axis='index')

                # Select time slice to remove extra hours from tz conversion
                df = df.loc[start:end]

                # Convert to DataArray
                da_comp = xr.DataArray(
                    df, dims=('time', 'region')).expand_dims(
                        'component').assign_coords(component=[component_name])

                # Concatenate
                da = (da_comp if da is None else
                      xr.concat([da, da_comp], dim='component'))

            # Convert capacity factor to hourly data
            da = da.resample(time='H').mean('time')

            # Add variable to dataset
            ds[variable_name] = da

        return ds

    def _get_url(self, component_name, date_from, date_to, source_id,
                 **kwargs):
        """Get URL.

        :param component_name: Component name.
        :param date_from: Date from which to start.
        :param date_to: Date to which to finish.
        :param source_id: Source ID.
        :type component_name: str
        :type date_from: str
        :type date_to: str
        :type source_id: str

        :returns: URL.
        :rtype: str
        """
        category = self.cfg['categories'][component_name]
        method = self.cfg['methods'][component_name]
        url_category = '{}/{}.{}.svc/{}'.format(
            self.cfg['host'], category, self.cfg['version'], method)
        try:
            url_options = '&'.join(
                '{}={}'.format(k, v) for k, v in self.cfg[
                    'options'][component_name].items())
        except AttributeError:
            url_options = ''
        url_cat_opt = '{}?{}'.format(url_category, url_options)

        if component_name == 'pv':
            url_date = '{}&dateFrom={}&dateTo={}'.format(
                url_cat_opt, date_from, date_to)
        elif component_name in ['wind', 'wind-onshore', 'wind-offshore']:
            url_date = '{}&beginDate={}&endDate={}'.format(
                url_cat_opt, date_from, date_to)

        # Add source ID to URL
        if component_name == 'pv':
            url = '{}&sourceId={}'.format(url_date, source_id)
        elif component_name in ['wind', 'wind-onshore', 'wind-offshore']:
            url = '{}&sourceIds=[{}]'.format(
                url_date, source_id)

        return url

    def _download_request(self, component_name, date_from, date_to, source_id,
                          **kwargs):
        """Get items from REST API with :py:class:`bs4.BeautifulSoup`.

        :param component_name: Component name.
        :param date_from: Date from which to start.
        :param date_to: Date to which to finish.
        :param source_id: Source ID.
        :type component_name: str
        :type date_from: str
        :type date_to: str
        :type source_id: str

        :returns items: Downloaded items.
        :rtype items: :py:class:`bs4.element.Tag`
        """
        # Get URL
        url = self._get_url(component_name, date_from, date_to, source_id,
                            **kwargs)

        tag_names = self.cfg['tags'][component_name]
        n_trials = 0
        while n_trials < self.max_fetch_trials:
            try:
                # Request and raise exception if needed
                response = self._session.get(url)
                response.raise_for_status()

                # Sparse XML
                soup = BeautifulSoup(response.text, 'xml')
                tag = getattr(soup, tag_names[0])
                items = getattr(tag, tag_names[1])

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

        return items

    def _get_region_ids(self, **kwargs):
        """Get region IDs.

        :returns: Region-IDs mapping.
        :rtype: dict
        """
        method = 'GetRegions'
        category = 'SolarForecasting'
        url = '{}/{}.{}.svc/{}'.format(
            self.cfg['host'], category, self.cfg['version'], method)

        # Request and raise exception if needed
        response = self._session.get(url)
        response.raise_for_status()

        regions_list = response.json()
        region_ids = {v['Name']: v['SourceId'] for v in regions_list}

        return region_ids

    def _get_download_filepath(self, variable_name, component_name,
                               region_name, date_from, date_to, **kwargs):
        """Get downloaded dataset filepath.

        :param variable_name: Dataset name.
        :param component_name: Component name.
        :param region_name: Region name.
        :param date_from: Date from which to start.
        :param date_to: Date to which to end.
        :type variable_name: str
        :type component_name: str
        :type region_name: str
        :type date_from: str
        :type date_to: str

        :returns: Filepath
        :rtype: str
        """
        src_dir = self.med.cfg.get_external_data_directory(self)
        src_dir = os.path.join(src_dir, variable_name)
        os.makedirs(src_dir, exist_ok=True)
        filename = '{}_{}_{}_{}_{}-{}.csv'.format(
            self.name, variable_name, component_name, region_name,
            date_from, date_to)
        filepath = os.path.join(src_dir, filename)

        return filepath

    def _get_dates(self, **kwargs):
        """Define dates adding one day because request in Brussels time
        # (CET/CEST) at a daily frequency and timestamps returned in UTC.

        :returns: Dates.
        :rtype: :py:class:`pandas.DatetimeIndex`
        """
        freq = 'MS'
        start = pd.Timestamp(self.cfg['start_date'], tz='utc')
        end = pd.Timestamp(self.cfg['end_date'], tz='utc')
        dates = pd.date_range(start=start, end=end + pd.Timedelta(31, 'D'),
                              freq=freq)

        return dates

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['start_date'], self.cfg['end_date'])

        return postfix
