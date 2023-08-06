"""Modifier offsetting variable definition."""
from copy import deepcopy
from ..actuator_base import ExtractorBase


class Actuator(ExtractorBase):
    """Modifier offsetting variable"""

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
            result_mng=result_mng, name=name, cfg=cfg,
            **kwargs)

        #: Variable to modify.
        self.modified_variable = self.cfg['variable_name']

        #: Offset to add to the variable.
        self.offset = self.cfg['offset']

    def transform(self, data_src=None, ds=None, **kwargs):
        """Apply modifier to data source.

        :param data_src: Data source to modify. Default is `None`,
          in which case :py:obj:`ds` should be given.
        :param ds: Dataset. Default is `None`,
          in which case :py:obj:`data_src` should be given.
        :type data_src: :py:class:`..data_source.DataSource`
        :type ds: :py:class:`xarray.Dataset`

        :returns: Modified dataset.
        :rtype: Same as :py:obj:`data_src.data`
        """
        if not self.cfg.get('no_verbose'):
            self.log.info('Adding {} to {}'.format(
                self.offset, self.modified_variable))

        # Copy source dataset (all variables)
        if ds is None:
            try:
                # As xarray.Dataset
                ds = data_src.data.copy(deep=True)
            except TypeError:
                # As dictionary
                ds = deepcopy(data_src.data)

        # Modify variable in dataset
        ds[self.modified_variable] += self.offset

        return ds

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        return '{}_offset_{}_{:d}'.format(
            super(Actuator, self).get_extractor_postfix(**kwargs),
            self.modified_variable, int(self.offset * 10 + 0.1))
