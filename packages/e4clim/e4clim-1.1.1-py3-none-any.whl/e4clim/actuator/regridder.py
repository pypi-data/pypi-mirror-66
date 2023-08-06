"""Modifier to regrid."""
from ..actuator_base import ExtractorBase


class Actuator(ExtractorBase):

    def __init__(self, result_mng, name, cfg=None, **kwargs):
        """Naming constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Actuator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping
        """
        super(Actuator, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg, **kwargs)

    def transform(self, ds=None, **kwargs):
        """Apply modifier to data source.

        :param ds: Dataset to transform.
        :type ds: :py:class:`xarray.Dataset`

        :returns: Modified dataset.
        :rtype: Same as :py:obj:`data_src.data`
        """
        if self.cfg['method'] == 'coarsen':
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Coarsening {} {} features'.format(
                        self.component_mng.name, self.result_mng.name))
            ds_new = ds.coarsen(**self.cfg['kwargs']).mean()
        elif self.cfg['method'] == 'interp':
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Interpolating {} {} features'.format(
                        self.component_mng.name, self.result_mng.name))
            ds_new = ds.interp(**self.cfg['kwargs'])

        return ds_new

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        skwargs = ''.join(['_{}{}'.format(k, v)
                           for k, v in self.cfg['kwargs'].items()])
        return '{}_{}{}'.format(
            super(Actuator, self).get_extractor_postfix(**kwargs),
            self.cfg['method'], skwargs)
