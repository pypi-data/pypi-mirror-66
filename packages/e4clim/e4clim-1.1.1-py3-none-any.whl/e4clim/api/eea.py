"""EEA API."""
from ..geo import DefaultMaskAPI, DefaultMaskMaker


class DataSource(DefaultMaskAPI, DefaultMaskMaker):
    #: Default source name.
    DEFAULT_SRC_NAME = 'eea'

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

    def get_url(self, sub_region=None, **kwargs):
        """Get URL of geographical data.

        :param sub_region: Secondary region to select. If `None`,
          the whole region is selected. Default is `None`.
        :type sub_region: str

        :returns: URL pointing to the geographical data.
        :rtype: str
        """
        sub_region = kwargs.get('sub_region', self.AREA)

        url = '{}/{}/{}{}'.format(self.cfg['host'], self.cfg['path'],
                                  sub_region.lower(), self.cfg['postfix'])

        return url

    def get_filename(self, sub_region=None, **kwargs):
        """Get downloaded-file name.

        :param sub_region: Secondary region to select. If `None`,
          the whole region is selected. Default is `None`.
        :type sub_region: str

        :returns: Filename.
        :rtype: str
        """
        return sub_region.lower()[:2] + '_' + self.cfg['resolution']
