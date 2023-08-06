"""natomraden.se API for Sweden's bidding zones."""
from pkg_resources import resource_filename
import geopandas as gpd
from ..geo import DefaultMaskAPI, DefaultMaskMaker, GEO_VARIABLE_NAME


class DataSource(DefaultMaskMaker, DefaultMaskAPI):
    #: Default source name.
    DEFAULT_SRC_NAME = 'natomraden'

    #: Area: `'Sweden'`.
    AREA = 'Sweden'

    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor calling :py:class:`DefaultMaskMaker`'s
        constructor.

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
        """Convenience function to warn that natomraden.se data is not downloaded
        but loaded from package data.

        :returns: Names of downloaded variables.
        :rtype: :py:class:`set` of :py:class:`str`

        .. note:: The JSON geometries were downloaded from the `natomraden.se <https://www.natomraden.se/>` source code.
        """
        self.log.warning(
            '{} is not to be downloaded. It is instead directly loaded from '
            'the package data.'.format(self.DEFAULT_SRC_NAME))

        return {GEO_VARIABLE_NAME}

    def read_file(self, *args, **kwargs):
        """Read geographical data for area from package resources.

        :param area: Geographical area for which to read the data.
        :type area: str

        :returns: Geographic data frame.
        :rtype: :py:class:`geopandas.GeoDataFrame`
        """
        # Get resource name
        resource_name = self.get_download_resource_name(self, **kwargs)

        # Read geographical file for area
        gdf = gpd.read_file(resource_filename(__name__, resource_name))

        return gdf

    def get_download_resource_name(self, variable_name, **kwargs):
        """Get package resource name for data scratched from natomraden.se.

        :returns: Resource name.
        :rtype: str
        """
        filename = 'sweden_bidding_zones_geometry.json'
        resource_name = '../data/{}/{}/{}'.format(
            self.AREA, self.DEFAULT_SRC_NAME, filename)

        return resource_name
