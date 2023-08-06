"""Actuator base definitions."""
import os
import sys
from collections import OrderedDict
from abc import ABC, abstractmethod
import pickle
import xarray as xr
from .container import Container, ensure_collection
from .config import import_module_from_cfg


class ActuatorBase(Container):
    """Actuator base class."""

    def __init__(self, result_mng, name, cfg=None, task_names=set(),
                 **kwargs):
        """Actuator constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Estimator configuration. Default is `None`.
        :param task_names: Names of potential tasks for container to perform.
          Default is `set()`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping
        :type task_names: set
        """
        #: Data sources.
        self.data_sources = None

        # Attach component and output variable to actuator
        #: Result manager of variable to act on.
        self.result_mng = result_mng
        #: Result component.
        self.component_mng = self.result_mng.component_mng

        # Initialize as container with output variable as parent
        kwargs.update({
            'component_mng': self.component_mng, 'name': name,
            'parent': result_mng, 'result_mng': result_mng, 'cfg': cfg,
            'med': self.component_mng.med, 'task_names': task_names})
        super(ActuatorBase, self).__init__(**kwargs)

        # Add data sources
        if 'data' in self.cfg:
            self.data_sources = OrderedDict()
            self.add_data_sources(**kwargs)

    def add_data_sources(self, cfg=None, **kwargs):
        """Add data sources from configuration.

        :param cfg: Configuration from which to get data source.
          Default is `None`, in which case the actuator configuration is
          used.
        :type cfg: mapping
        """
        cfg = cfg or self.cfg
        for stage, src_vars in cfg['data'].items():
            # Add data source to mediator and result manager
            self.data_sources[stage] = self.med.add_data_source(
                src_vars, self.result_mng)

            # Add data sources as children
            self.update_children({self.data_sources[stage].name:
                                  self.data_sources[stage]})


class EstimatorBase(ActuatorBase, ABC):
    """Estimator abstract base class. Requires :py:meth:`fit` and
    :py:meth:`predict` methods to be implemented."""

    def __init__(self, result_mng, name, cfg=None, **kwargs):
        """Estimator constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Estimator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping
        """
        #: Coefficients to be fitted
        self.coef = None

        # Try updating task names in keyword arguments if possible
        task_names = kwargs.get('task_names') or set()
        task_names.update({'fit', 'predict'})
        kwargs.update({
            'component_mng': result_mng.component_mng, 'name': name,
            'result_mng': result_mng,
            'cfg': cfg, 'med': result_mng.med, 'task_names': task_names})
        # Initialize as container
        super(EstimatorBase, self).__init__(**kwargs)

    @abstractmethod
    def fit(**kwargs):
        """Fit estimator abstract method."""
        raise NotImplementedError

    @abstractmethod
    def predict(**kwargs):
        """Predict with estimator abstract method."""
        raise NotImplementedError

    def get_estimator_postfix(self, **kwargs):
        """Default implementation: get an empty postfix string.

        :returns: Postfix.
        :rtype: str
        """
        return ''

    def get_fit_postfix(self, **kwargs):
        """Get fit postfix (component, feature, estimator).

        :returns: Postfix.
        :rtype: str
        """
        # Feature postfix
        feature_postfix = self.result_mng.feature[
            'fit'].get_data_postfix(**kwargs)

        # Output data postfix
        data_src = self.result_mng.extractor['output'].data_sources[
            'output']
        output_postfix = data_src.get_data_postfix(
            with_src_name=True, **kwargs)

        # Estimator postfix
        estimator_postfix = self.get_estimator_postfix(**kwargs)

        # Fit postfix
        fit_postfix = '{}{}{}'.format(
            feature_postfix, output_postfix, estimator_postfix)

        return fit_postfix

    def get_fit_path(self, makedirs=True, **kwargs):
        """Get fit filepath.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Filepath.
        :rtype: str
        """
        filename = '{}_estimator{}'.format(
            self.component_mng.name, self.get_fit_postfix(**kwargs))
        data_dir = self.component_mng.get_data_dir(makedirs=makedirs, **kwargs)
        filepath = os.path.join(data_dir, filename)

        return filepath

    def read(self, **kwargs):
        """Read estimator with pickle."""
        try:
            # Try to read as netcdf data-array
            filepath = '{}.nc'.format(self.get_fit_path(**kwargs))
            if not self.cfg.get('no_verbose'):
                self.log.info('Reading {} {} {} estimator from {}'.format(
                    self.component_mng.name, self.result_mng.name, self.name,
                    filepath))
            self.coef = xr.load_dataarray(filepath)
        except FileNotFoundError:
            # Read as pickle otherwise
            filepath = '{}.pickle'.format(self.get_fit_path(**kwargs))
            if not self.cfg.get('no_verbose'):
                self.log.info('Reading {} {} {} estimator from {}'.format(
                    self.component_mng.name, self.result_mng.name, self.name,
                    filepath))
            with open(filepath, 'rb') as f:
                self.coef = pickle.load(f)

    def write(self, **kwargs):
        """Write estimator with pickle."""
        try:
            # Try to write as netcdf data-array
            filepath = '{}.nc'.format(self.get_fit_path(**kwargs))
            if not self.cfg.get('no_verbose'):
                self.log.info('Writing {} {} {} estimator to {}'.format(
                    self.component_mng.name, self.result_mng.name, self.name,
                    filepath))
            self.coef.to_netcdf(filepath)
        except AttributeError:
            # Read as pickle otherwise
            filepath = '{}.pickle'.format(self.get_fit_path(**kwargs))
            if not self.cfg.get('no_verbose'):
                self.log.info('Writing {} {} {} estimator to {}'.format(
                    self.component_mng.name, self.result_mng.name, self.name,
                    filepath))
            # Otherwise, write as pickle
            with open(filepath, 'wb') as f:
                pickle.dump(self.coef, f)


class ExtractorBase(ActuatorBase, ABC):
    """Extractor base class.
    By default, the :py:meth:`transform` method does nothing
    and input data is just read.
    """

    def __init__(self, result_mng, name, cfg=None, variable_names=None,
                 stages={'fit', 'predict', 'output'}, **kwargs):
        """Extractor constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Estimator configuration. Default is `None`.
        :param variable_names: Name(s) of variable(s) to be extracted.
          Default is `None`.
        :param stages: Stages at which extraction is performed.
          Default is `{'fit', 'predict', 'output'}`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping
        :type variable_names: (collection of) :py:class:`str`
        :type stages: (collection of) :py:class:`str`
        """
        #: Estimation stages.
        self.stages = set(stages)

        #: Transformation flag. If `True`, no extraction is performed.
        self.no_extraction = False

        # Initialize as container
        task_names = set()
        for stage in self.stages:
            task_names.update({'extract__' + stage, 'write__' + stage})
        kwargs.update({
            'component_mng': result_mng.component_mng, 'name': name,
            'result_mng': result_mng,
            'cfg': cfg, 'med': result_mng.med, 'task_names': task_names})
        super(ExtractorBase, self).__init__(**kwargs)

        #: Extractor variables.
        self.variable_names = ensure_collection(variable_names, set) or set()

    @abstractmethod
    def transform(self, data_src, stage=None, **kwargs):
        """Abstract transform method."""
        raise NotImplementedError

    def get_extractor_postfix(self, **kwargs):
        """Default implementation: get an empty extractor postfix string.

        :returns: Postfix.
        :rtype: str
        """
        return ''


class DefaultExtractor(ExtractorBase):
    """Default extractor implementation.
    By default, the :py:meth:`transform` method does nothing
    and input data is just read.
    """

    def __init__(self, result_mng, name, cfg=None, **kwargs):
        """Default extractor constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Estimator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping
        """
        super(DefaultExtractor, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg,
            variable_names=result_mng.result_name, **kwargs)

        # Flag that no transformation is to be performed, unless explicitly
        # asked with `'write'` entry of configuration (for instance if
        # modifier active)
        self.no_extraction = not self.cfg.get('write')

    def transform(self, ds=None, data_src=None, stage=None, **kwargs):
        """Default transform: return equal or modified data source
        for the component and all variables and prevent writing.

        :param data_src: Input data source.
        :param stage: Modeling stage: `'fit'`, `'predict'`, or `'output'`.
        :type data_src: :py:class:`..data_source.DataSourceBase`
        :type stage: str

        :returns: Dataset.
        :rtype: :py:class:`xarray.Dataset`

        .. warning:: If a modifier is active, its 'transform' method
          replaces any such method present in :py:obj:`kwargs['transform']`.
        """
        if hasattr(self.result_mng, 'modifier'):
            if (hasattr(self.result_mng.modifier.cfg, 'stage') and
                    (self.result_mng.modifier.cfg['stage'] != stage)):
                pass
            else:
                # Add modifier transformation to keyword arguments
                kwargs['transform'] = self.result_mng.modifier.transform

        # Get data
        data = data_src.get_data(**kwargs)

        ds = {}
        for variable_name, da in data.items():
            # Try to select component
            try:
                da = da.sel(component=self.component_mng.component_name)
            except ValueError:
                pass

            # Add data array to dataset
            ds[variable_name] = da

        # Prevent writing if same data
        if self.no_extraction:
            self.task_mng['write__' + stage] = False

        # Return equal data for component
        return ds


def add_actuator(container, actuator_name=None, actuator=None,
                 cfg=None, actuator_class_name='Actuator', **kwargs):
    """Add actuator (extractor, estimator, modifier, etc.).

    :param container: Container to which to add actuator.
    :param actuator_name: Actuator name. Default is `None`,
      in which case a `TypeError` will be raised if `actuator` is
      not `None`.
    :param actuator: Actuator. Default is `None`, in which case
      it is built with :py:meth:`_init_actuator`.
    :param cfg: Configuration in which to look for actuator configurations.
      Default is `None`, in which case it is taken from the parent
      configuration.
    :param actuator_class_name: Actuator class to call from module.
      Default is `'Actuator'`.
    :type container: :py:class:`.container.Container`
    :type actuator_name: str
    :type actuator: :py:class:`.container.Container`
    :type cfg: mapping
    :type actuator_class_name: str
    """
    cfg = cfg or container.cfg
    if actuator is None:
        if actuator_name is None:
            msg = "missing 1 required positional argument: 'actuator_name'"
            raise TypeError(msg)
        if actuator_name in cfg:
            actuator_cfg = cfg[actuator_name]
            actuator_module = import_module_from_cfg(
                actuator_cfg, name=actuator_name)

            if actuator_module is None:
                # Get default actuator
                actuator_class_name = 'Default' + ''.join(
                    act_name.title()
                    for act_name in actuator_name.split('_'))
                actuator_module = sys.modules[__name__]
                container.log.warning(
                    '    No "module_path" found in {} configuration: '
                    'using {} class actuator'.format(
                        actuator_name, actuator_class_name))

            # Try to get actuator
            if hasattr(actuator_module, actuator_class_name):
                actuator = getattr(actuator_module, actuator_class_name)(
                    container, actuator_name, cfg=actuator_cfg)
            else:
                raise AttributeError(
                    'No {} class found in {} module for {} {} '
                    'actuator'.format(
                        actuator_class_name, actuator_module,
                        container.name, actuator_name))

    if actuator is not None:
        if not container.cfg.get('no_verbose'):
            container.log.info('Injecting {} actuator in {} {}'.format(
                actuator.name, container.component_mng.name, container.name))
        return actuator


# Alias default feature and output extractor
DefaultFeatureExtractor = DefaultOutputExtractor = DefaultExtractor
