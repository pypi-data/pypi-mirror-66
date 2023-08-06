import xarray as xr
from ..container import ensure_collection
from ..actuator_base import ExtractorBase


class Actuator(ExtractorBase):
    """Default feature extractor implementation.
    By default, the :py:meth:`transform` method does nothing
    and input data is just read.
    """

    def __init__(self, result_mng, name, cfg=None, **kwargs):
        """Default feature extractor constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Estimator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping

        .. note::

          * The name of the variables to concatenate are given in the
            `'variables_to_concat'` entry of the container configuration.
            If this entry is empty, the name of the actuator result manager
            is used instead.
          * The dimension along which to concatenate must be given
            in the `'dim_to_concat'` entry of the container configuration.
        """
        # Variables to concatenate.
        variable_names = (
            ensure_collection(cfg.get('variables_to_concat'), set)
            or set([result_mng.result_name]))

        # Extractor initialization
        super(Actuator, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg,
            variable_names=variable_names, **kwargs)

        #: Dimension along which to concatenate.
        self.dim_to_concat = self.cfg.get('dim_to_concat')

    def transform(self, data_src, **kwargs):
        """Default transform: return identical data source
        and prevent writing.

        :param data_src: Input multiple data source.
        :type data_src: :py:class:`..data_source.MultiDataSource`
        """
        self.log.info(
            '{} {} feature concatenation along {} dimension:'.format(
                self.component_mng.component_name, self.result_mng.result_name,
                self.dim_to_concat))

        # Get data (letting multiple data source manage variables)
        kwargs_data_src = kwargs.copy()
        kwargs_data_src.pop('variable_names', None)
        data_src.get_data(**kwargs_data_src)

        ds = {}
        for variable_name in self.variable_names:
            self.log.info(
                '  - Concatenating {} variable:'.format(variable_name))

            # Collect data for variable from all single data sources
            data = []
            for src_name, single_data_src in (
                    data_src.var_data_sources[variable_name].items()):
                self.log.info(
                    '    - Adding {} data source'.format(src_name))
                data.append(single_data_src[variable_name])

            # Concatenate
            ds[variable_name] = xr.concat(data, dim=self.dim_to_concat)

        return ds
