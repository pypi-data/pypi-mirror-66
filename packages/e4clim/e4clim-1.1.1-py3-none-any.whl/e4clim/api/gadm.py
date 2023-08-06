"""Database of Global Administrative Areas (GADM) API."""
from ..geo import DefaultMaskAPI, DefaultMaskMaker, get_country_code


class DataSource(DefaultMaskMaker, DefaultMaskAPI):
    #: Default source name.
    DEFAULT_SRC_NAME = 'gadm'

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

        #: Child column.
        self._child_column = '{}_{}'.format(
            self.cfg['child_column_prefix'], str(self.cfg['level']))

    def get_url(self, area, **kwargs):
        """Get URL of geographical data for given area.

        :param area: Area for which to get data.
        :type area: str

        :returns: URL pointing to geographical data.
        :rtype: :str
        """
        # Get the country code
        country_code = get_country_code(area, code='alpha-3')

        # Get URL
        path = '{}/{}/{}{}/{}/'.format(
            self.cfg['host'], self.cfg['path'], self.name.lower(),
            self.cfg['version'], self.cfg['format'])
        sver = self.cfg['version'].replace('.', '')
        prefix = '{}{}_{}'.format(self.name.lower(), sver, country_code)
        url = '{}{}_{}.zip'.format(path, prefix, self.cfg['format'])

        return url

    def get_filename(self, area, **kwargs):
        """Get downloaded-file name for given area.

        :param area: Area for which to get data.
        :type area: str

        :returns: Filename.
        :rtype: str
        """
        # Get the country code
        country_code = get_country_code(area, code='alpha-3')

        # Get filename
        sver = self.cfg['version'].replace('.', '')
        prefix = '{}{}_{}'.format(self.name.lower(), sver, country_code)
        filename = '{}_{}.shp'.format(prefix, str(self.cfg['level']))

        return filename
