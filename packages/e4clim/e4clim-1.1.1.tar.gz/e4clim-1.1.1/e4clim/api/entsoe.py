"""ENTSOE API."""
import os
import numpy as np
import pandas as pd
import xarray as xr
from entsoe import EntsoePandasClient
from entsoe.mappings import PSRTYPE_MAPPINGS
from entsoe.exceptions import NoMatchingDataError
from ..geo import get_country_code
from ..data_source import DataSourceLoaderBase
from ..component import (DataSourceWithComponentsMixin,
                         parse_variable_component_args,
                         finalize_dataset)


class DataSource(DataSourceLoaderBase, DataSourceWithComponentsMixin):
    #: Default source name.
    DEFAULT_SRC_NAME = 'entsoe'

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

        self.sampling_conversion = {'P1Y': 'Y', 'PT60M': 'H'}

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
          `ENTSO-E Transparency Platform <https://transparency.entsoe.eu/>`.
        """
        # Define start and end dates (ISO format)
        start = pd.Timestamp(self.cfg['period_start'], tz=self.cfg['tz'])
        end = pd.Timestamp(self.cfg['period_end'], tz=self.cfg['tz'])
        svar = ', '.join(str(variable_name)
                         for variable_name in variable_component_names)
        if not self.cfg.get('no_verbose'):
            self.log.info(
                '{} variables from {} to {}:'.format(svar, start, end))

        # Get credentials and start ENTSO-E client
        cred = self.med.cfg.get_credentials(
            self.DEFAULT_SRC_NAME, ['security_token'])
        client = EntsoePandasClient(api_key=cred['security_token'])

        # Get zone-code mapping and zone-countrycode mapping
        place_code, place_country_code, place_lookup = self._get_place_code(
            **kwargs)

        # Loop over variables
        for variable_name, component_names in variable_component_names.items():
            # Define query
            src_variable_name = self.cfg['variable_names'][variable_name]
            if not self.cfg.get('no_verbose'):
                self.log.info('- {}:'.format(variable_name))
            query = getattr(client, 'query_{}'.format(src_variable_name))

            # Manage wind component as onshore plus offshore
            component_name = 'wind'
            component_to_download_names = component_names.copy()
            if component_name in component_names:
                # Make sure that generation and capacity are downloaded
                component_to_download_names.update(
                    ['wind-onshore', 'wind-offshore'])

                # Remove capacity factor from components to download
                component_to_download_names.discard(component_name)

            # Loop over components
            for component_name in component_to_download_names:
                src_component_name = self.cfg['component_names'][
                    component_name]
                psr_type = [k for k, v in PSRTYPE_MAPPINGS.items()
                            if v == src_component_name][0]
                if not self.cfg.get('no_verbose'):
                    self.log.info('-- {} -> {} -> {}:'.format(
                        component_name, src_component_name, psr_type))
                # Loop over zones
                without_zones = True
                for place_name, code in place_code.items():
                    country_code = place_country_code[place_name]
                    if not self.cfg.get('no_verbose'):
                        self.log.info('--- {}'.format(place_name))
                    try:
                        # Try with zones
                        df = query(
                            code, start=start, end=end, psr_type=psr_type,
                            lookup_bzones=place_lookup[place_name])
                    except TypeError:
                        if without_zones:
                            # Get dataset without zones instead
                            if place_lookup[place_name]:
                                self.log.warning(
                                    '{} dataset not zonal: downloading '
                                    'for country instead'.format(
                                        variable_name))
                            df = query(country_code, start=start, end=end,
                                       psr_type=psr_type)
                            without_zones = False
                        else:
                            # Otherwise break zones loop
                            break
                    except NoMatchingDataError:
                        if not self.cfg.get('no_verbose'):
                            self.log.warning(
                                'No mathcing data found for {} {} {}.'
                                ' Saving empty data frame.'.format(
                                    place_name, component_name, variable_name))
                        df = pd.DataFrame(columns=[component_name])

                    # Adjust names
                    df.index.name = 'time'
                    df.columns = [component_name]

                    # Save locally
                    filepath = self._get_download_filepath(
                        variable_name, component_name, place_name, code,
                        **kwargs)
                    df.to_csv(filepath)

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
        :rtype: :py:class:`xarray.Dataset()`
        """
        # Get zone-code mapping
        place_code, _, _ = self._get_place_code(**kwargs)

        # Loop over datasets
        ds = {}
        for variable_name, component_names in variable_component_names.items():
            if not self.cfg.get('no_verbose'):
                self.log.info('- {}:'.format(variable_name))

            # Manage wind component as onshore plus offshore
            component_name = 'wind'
            component_to_load_names = component_names.copy()
            if component_name in component_names:
                # Make sure that generation and capacity are loaded
                component_to_load_names.update(
                    ['wind-onshore', 'wind-offshore'])

                # Remove capacity factor from components to load
                component_to_load_names.discard(component_name)

            # Loop over components
            da = None
            for component_name in component_to_load_names:
                if not self.cfg.get('no_verbose'):
                    self.log.info('-- {}:'.format(component_name))
                # Loop over zones
                da_comp = None
                for place_name, code in place_code.items():
                    if not self.cfg.get('no_verbose'):
                        self.log.info('--- {}'.format(place_name))
                    # Read downloaded data
                    filepath = self._get_download_filepath(
                        variable_name, component_name, place_name, code,
                        **kwargs)
                    df = pd.read_csv(filepath, index_col=0, parse_dates=True)

                    # Convert index timezone to UTC
                    df.index = pd.to_datetime(
                        df.index, utc=True).tz_convert(None)

                    # Convert to DataArray
                    da_zone = xr.DataArray(
                        df, dims=('time', 'component')).expand_dims(
                            'region').assign_coords(region=[place_name])

                    area = self.med.geo_src.place_area[place_name]
                    if (area == 'Italy') and (variable_name == 'generation'):
                        # Set inconsistent values to NaN
                        da_zone.values.setflags(write=True)
                        start_na = pd.Timestamp('2016-10-26T00:00')
                        end_na = pd.Timestamp('2016-11-01T00:00')
                        da_zone.loc[{'time': slice(start_na, end_na)}] = np.nan

                    # Concatenate
                    da_comp = (da_zone if da_comp is None else
                               xr.concat([da_comp, da_zone], dim='region'))

                # Concatenate
                da = (da_comp if da is None else
                      xr.concat([da, da_comp], dim='component'))

            # Add total wind component if needed
            component_name = 'wind'
            if component_name in component_names:
                # Treat NaNs as zero unless in both components
                da_on = da.sel(component='wind-onshore', drop=True)
                da_off = da.sel(component='wind-offshore', drop=True)
                na = da_on.isnull() & da_off.isnull()
                da_wind = (da_on.fillna(0.) + da_off.fillna(0.)).where(
                    ~na, np.nan)
                da_wind = da_wind.expand_dims('component').assign_coords(
                    component=[component_name])
                da = xr.concat([da, da_wind], dim='component')

            # Add variable to dataset
            ds[variable_name] = da

        return ds

    def _get_place_code(self, **kwargs):
        """Get zone to zone-code mapping and zone to country-code mapping.

        :returns: Zone to zone code, zone to country code and
          zone to lookup flag mappings.
        :rtype: :py:class:`tuple` of

          * mapping of :py:class:`str` to :py:class:`str`
          * mapping of :py:class:`str` to :py:class:`str`
          * mapping of :py:class:`str` to :py:class:`bool`

        .. seealso:: :py:meth:`..geo.get_country_code`.
        """
        # Get place names for source
        src_place_regions, _ = (
            self.med.geo_src.get_place_regions_for_source(
                self.name, **kwargs))

        place_code = {}
        place_country_code = {}
        place_lookup = {}
        for place_name, region_names in src_place_regions.items():
            # Get place (zone) area (country)
            area = self.med.geo_src.place_area[place_name]

            # Get country code
            place_country_code[place_name] = get_country_code(
                area, code='alpha-2')

            if area == place_name:
                # Assign country-code to place (country)
                place_code[area] = place_country_code[place_name]

                # Do not look for building zone for this place
                place_lookup[area] = False
            else:
                # Assign code to place (zone)
                place_code[place_name] = '{}-{}'.format(
                    place_country_code[place_name], region_names[0])

                # Look for building zone for this place
                place_lookup[place_name] = True

        return place_code, place_country_code, place_lookup

    def _get_download_filepath(
            self, variable_name, component_name, place_name, code, **kwargs):
        """Get downloaded dataset filepath.

        :param variable_name: Dataset name.
        :param component_name: Component name.
        :param place_name: Zone/country name.
        :param code: Zone/country code.
        :type variable_name: str
        :type component_name: str
        :type place_name: str
        :type code: str

        :returns: Filepath
        :rtype: str
        """
        src_dir = self.med.cfg.get_external_data_directory(self)
        src_dir = os.path.join(src_dir, variable_name)
        os.makedirs(src_dir, exist_ok=True)
        filename = '{}_{}_{}_{}{}.csv'.format(
            self.name, variable_name, component_name, code,
            self.get_postfix(**kwargs))
        filepath = os.path.join(src_dir, filename)

        return filepath

    def get_postfix(self, **kwargs):
        """Get data-source standard postfix.

        :returns: Postfix.
        :rtype: str
        """
        postfix = '_{}-{}'.format(
            self.cfg['period_start'], self.cfg['period_end'])

        return postfix
