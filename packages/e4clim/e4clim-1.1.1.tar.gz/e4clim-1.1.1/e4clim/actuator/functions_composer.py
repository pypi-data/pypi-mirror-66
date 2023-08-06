"""Extractor defining transform method from functions composition."""
from importlib import import_module
from collections import OrderedDict
from ..data_source import Composer
from ..actuator_base import ExtractorBase
from e4clim.container import ensure_collection


class Actuator(ExtractorBase):
    """Extractor defining transform method from functions composition."""

    def __init__(self, result_mng, name, cfg=None, functions=None,
                 **kwargs):
        """Constructor defining transform method from functions composition.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Actuator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping

        .. note:: Functions to compose must be provided as a list
          from the `functions` entry of the configuration.
        """
        super(Actuator, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg, **kwargs)

        #: Functions composed to define :py:meth:`transform` method.
        self.functions = None

        if functions is None:
            # Import functions
            function_paths = ensure_collection(self.cfg['functions'])
            self._functions = [import_function(function_path)
                               for function_path in function_paths]
        else:
            # Assign user-defined functions
            self._functions = functions

        # Define :py:meth:`transform` method by composing functions
        self.transform = Composer(*self._functions)

        # Add data sources
        if 'data' in self.cfg:
            if self.data_sources is None:
                self.data_sources = OrderedDict()
            self.add_data_sources(**kwargs)

    def transform(self, **kwargs):
        """Empty concrete definition of transform method replaced
        by composed functions during construction."""
        pass


def import_function(function_path):
    """Import function.

    :param function_path: Function path.
    :type function_path: str

    :return: Imported function.
    :rtype: function
    """
    # Get module path and function name
    fun_path_split = function_path.split('.')
    module_path = '.'.join(fun_path_split[:-1])
    function_name = fun_path_split[-1]

    # Import function module
    module = import_module(module_path)

    # Return function
    return getattr(module, function_name)
