"""Extractor composing multiple extractors."""
from collections import OrderedDict
from ..actuator_base import ExtractorBase, add_actuator
from ..data_source import Composer


class Actuator(ExtractorBase):

    def __init__(self, result_mng, name, cfg=None, **kwargs):
        """Naming constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Actuator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping

        .. note:: Actuators to compose must be provided as a dictionary
          from the `extractors` entry of the configuration.
        """
        super(Actuator, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg, **kwargs)

        # Initialize actuators from configuration
        self.actuators = OrderedDict()
        for actuator_name in self.cfg['extractors']:
            # Get actuator
            actuator = add_actuator(
                self.result_mng, actuator_name=actuator_name,
                cfg=self.cfg['extractors'], **kwargs)

            # Reference actuator in actuators set
            self.actuators[actuator_name] = actuator

        #: Functions composed to define :py:meth:`transform` method.
        self._functions = None

        # Add transform of each actuators in the right order
        self._functions = [self.actuators[actuator_name].transform
                           for actuator_name in self.cfg['extractors']]

        # Define :py:meth:`transform` method by composing functions
        self.transform = Composer(*self._functions)

        # Add data sources
        for actuator in self.actuators.values():
            if 'data' in actuator.cfg:
                if self.data_sources is None:
                    self.data_sources = OrderedDict()
                self.add_data_sources(cfg=actuator.cfg, **kwargs)

    def transform(self, **kwargs):
        """Empty concrete definition of transform method replaced
        by composed functions during construction."""
        pass

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        # Get default postfix
        postfix0 = super(Actuator, self).get_extractor_postfix(**kwargs)

        # Add postfixes of every actuator
        return ''.join([postfix0] + [
            self.actuators[actuator_name].get_extractor_postfix(**kwargs)
            for actuator_name in self.cfg['extractors']])
