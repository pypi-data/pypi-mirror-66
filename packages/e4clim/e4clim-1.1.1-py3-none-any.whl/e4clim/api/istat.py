"""ISTAT API."""
import os
from ..geo import DefaultMaskAPI, DefaultMaskMaker


class DataSource(DefaultMaskAPI, DefaultMaskMaker):
    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator. Default is `None`.
        :param name: Data source name.
        :param cfg: Data source configuration.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        name = name or 'istat'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def get_url_filename(self, *kwargs):
        """ Get URL and filename of geographical data.

        :returns: URL pointing to geographical data and
          the name of shapefile.
        :rtype: tuple of str
        """
        postfix = self.cfg['date'] + self.cfg['resolution']
        dir0 = 'Limiti' + postfix
        url = '{}/{}/{}.zip'.format(self.cfg['host'], self.cfg['path'], dir0)

        return url

    def get_filename(self, *args, **kwargs):
        """Get downloaded-file name.

        :returns: Filename.
        :rtype: str
        """
        postfix = self.cfg['date'] + self.cfg['resolution']
        dir0 = 'Limiti' + postfix
        dir1 = 'Reg' + postfix
        filename = os.path.join(dir0, dir1, dir1 + '.shp')

        return filename
