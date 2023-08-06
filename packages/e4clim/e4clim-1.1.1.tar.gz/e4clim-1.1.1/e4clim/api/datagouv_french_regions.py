"""data.gouv.fr API for French regions."""
import os
import requests
from ..geo import DefaultMaskAPI, DefaultMaskMaker, GEO_VARIABLE_NAME


class DataSource(DefaultMaskMaker, DefaultMaskAPI):
    #: Default source name.
    DEFAULT_SRC_NAME = 'datagouv_french_regions'

    #: Area: `'France'`.
    AREA = 'France'

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

    def get_filename(self, **kwargs):
        """Get filename of geographical data for a given region.

        :returns: Shapefile filename.
        :rtype: str
        """
        return 'regions.shp'

    def download(self, **kwargs):
        """Download shapefile defining regions and
        store geographical data to :py:attr::`data` member.

        :returns: Names of downloaded variables.
        :rtype: :py:class:`set` of :py:class:`str`
        """
        # Make source dir
        src_dir = self.med.cfg.get_external_data_directory(self, **kwargs)

        # Get downloaded-file name
        filename_shp = self.get_filename(**kwargs)

        # Download
        root_url = '{}/fr/datasets/r/'.format(self.cfg['host'])
        self.log.info('Downloading shapefile from {}'.format(
            root_url))
        for filetype in self.cfg['filetypes']:
            filename = '{}.{}'.format(filename_shp[:-4], filetype)
            filepath = os.path.join(src_dir, filename)
            if filetype == 'prj':
                with open(filepath, 'w') as f:
                    # Replace Lambert II Carto with Lambert II Etendu
                    f.write(self.cfg['wkt'])
            else:
                url = '{}{}'.format(root_url, self.cfg[filetype])

                # Request and raise exception if needed
                response = requests.get(url)
                response.raise_for_status()

                # Write file
                with open(filepath, 'wb') as f:
                    for chunk in response:
                        f.write(chunk)

        return {GEO_VARIABLE_NAME}
