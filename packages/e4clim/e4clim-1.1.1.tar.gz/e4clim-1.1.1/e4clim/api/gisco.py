"""GISCO API for European borders."""
import requests
from ..geo import DefaultMaskAPI, DefaultMaskMaker


class DataSource(DefaultMaskMaker, DefaultMaskAPI):
    """GISCO data source."""
    #: Default source name.
    DEFAULT_SRC_NAME = 'gisco'

    #: Flag preventing several downloads per area.
    ONE_DOWNLOAD_PER_AREA = True

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

    def get_url(self, **kwargs):
        """ Get URL of geographical data.

        :returns: URL pointing to the geographical data.
        :rtype: str
        """
        # Get the list of files
        path = self.cfg['host'] + '/' + self.cfg['path'] + '/'
        url_files = path + 'nuts-{}-files.json'.format(self.cfg['year'])
        n_trials = 0
        while n_trials < self.cfg['max_fetch_trials']:
            try:
                # Request and raise exception if needed
                response = requests.get(url_files)
                response.raise_for_status()
                break
            except requests.exceptions.SSLError as e:
                # Retry
                self.log.warning(
                    '{} trial to fetch {} file list failed: {}'.format(
                        n_trials + 1, self.namestr(e)))
                n_trials += 1
                continue
        # Verify that last trial succeeded
        if n_trials >= self.cfg['max_fetch_trials']:
            # All trials failed
            self.log.critical(
                'Fetching failed after {:d} trials'.format(n_trials))
            raise RuntimeError

        # Get the filename
        filename = self.get_filename(**kwargs)

        # Get URL
        url = '{}{}'.format(path, response.json()['geojson'][filename])

        return url

    def get_filename(self, *args, **kwargs):
        """Get downloaded-file name.

        :returns: Filename.
        :rtype: str
        """
        fmt = (self.cfg['spatial_type'], self.cfg['scale'],
               self.cfg['year'], self.cfg['projection'],
               self.cfg['nuts_level'])

        return 'NUTS_{}_{}_{}_{}_LEVL_{}.geojson'.format(*fmt)
