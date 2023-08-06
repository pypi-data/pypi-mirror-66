"""Modifier to resample."""
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

    def transform(self, ds=None, data_src=None, **kwargs):
        """Apply modifier to data source.

        :param ds: Dataset to transform.
        :type ds: :py:class:`xarray.Dataset`

        :returns: Modified dataset.
        :rtype: Same as :py:obj:`data_src.data`
        """
        coord = list(self.cfg['indexer'])[0]

        ds_new = ds.copy()
        for da_name, da in ds.items():
            # Resample array
            gp = da.resample(self.cfg['indexer'])

            # Apply reduction
            ds_new[da_name] = getattr(gp, self.cfg['apply'])(coord)

        return ds_new

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        postfix = '_{}{}{}'.format(
            *list(self.cfg['indexer'].items())[0], self.cfg['apply'])

        return '{}{}'.format(
            super(Actuator, self).get_extractor_postfix(**kwargs), postfix)
