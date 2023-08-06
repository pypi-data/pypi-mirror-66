"""RTE-bilan API."""
from pkg_resources import resource_stream
import pandas as pd
import xarray as xr
from ..data_source import DataSourceLoaderBase
from ..component import (DataSourceWithComponentsMixin,
                         parse_variable_component_args,
                         finalize_dataset)


class DataSource(DataSourceLoaderBase, DataSourceWithComponentsMixin):
    #: Default source name.
    DEFAULT_SRC_NAME = 'rte_bilan'

    #: Area: `'France'`.
    AREA = 'France'

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

    def download(self, *args, **kwargs):
        """Convenience function to warn that RTE-bilan data is not downloaded
        but loaded from package data.

        :returns: Names of variables to download.
        :rtype: :py:class:`set` of :py:class:`str`
        """
        self.log.warning(
            '{} is not to be downloaded. It is instead directly loaded from '
            'the package data.'.format(self.DEFAULT_SRC_NAME))

        return {'capacity_factor'}

    @parse_variable_component_args
    @finalize_dataset
    def load(self, variable_component_names, **kwargs):
        """Load data.

        :param variable_component_names: Names of components to load per
          variable. Default is `None`, in which case all components in
          :py:attr::`med.component_managers` are loaded.
        :type variable_component_names: mapping from :py:class:`str`
          to collection

        :returns: Time series for each variable and component.
        :rtype: dict
        """
        # Get places and regions
        src_place_regions, _ = self.med.geo_src.get_place_regions_for_source(
            self.name, self.AREA, **kwargs)

        ds = {}
        for variable_name, component_names in variable_component_names.items():
            # Manage wind component as onshore only
            component_name = 'wind'
            component_to_load_names = component_names.copy()
            if component_name in component_names:
                # Make sure that generation and capacity are loaded
                component_to_load_names.add('wind-onshore')

                # Remove capacity factor from components to load
                component_to_load_names.discard(component_name)

            da = None
            for component_name in component_to_load_names:
                # Read preprocessed RTE report for this variable and component
                resource_name = self.get_download_resource_name(
                    variable_name, component_name, **kwargs)
                with resource_stream(__name__, resource_name) as f:
                    df = pd.read_csv(f, index_col=0)

                # Define time index
                time = pd.to_datetime(
                    {'year': df.index.values.astype(str),
                     'month': 12, 'day': 31})
                df.index = pd.DatetimeIndex(time, freq='A-DEC')
                df.index.name = 'time'

                # Group by zones, averaging capacity factors
                df_zones = pd.DataFrame(
                    0., index=df.index, columns=list(src_place_regions))
                for place_name, region_names in src_place_regions.items():
                    df_zones[place_name] = df[region_names].mean('columns')

                # Create array and add component coordinate
                da_comp = xr.DataArray(
                    df_zones, dims=['time', 'region']).expand_dims(
                    'component').assign_coords(component=[component_name])

                # Add component data to array
                da = da_comp if da is None else xr.concat(
                    [da, da_comp], dim='component')

            # Add total wind component as onshore wind if needed
            component_name = 'wind'
            if component_name in component_names:
                coord_component = da.indexes['component'].tolist()
                idx = coord_component.index('wind-onshore')
                coord_component[idx] = component_name
                da['component'] = coord_component

            # Add variable to dataset
            ds[variable_name] = da

        return ds

    def get_download_resource_name(self, variable_name, component_name,
                                   **kwargs):
        """Get package resource name for data copied from RTE reports.

        :param variable_name: Variable name.
        :param component_name: Component name.
        :type variable_name: str
        :type component_name: str

        :returns: Resource name.
        :rtype: str
        """
        filename = '{}_{}_year_{}_{}.csv'.format(
            variable_name, component_name, self.cfg['first_year'],
            self.cfg['last_year'])
        resource_name = '../data/{}/{}/{}'.format(
            self.AREA, self.DEFAULT_SRC_NAME, filename)

        return resource_name
