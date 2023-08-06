"""Mediator-related definitions."""
import os
import collections
import logging
from warnings import warn
from .config import Config, import_module_from_cfg
from .component import ComponentManager
from .data_source import MultiDataSource
from .geo import MultiGeoDataSource
from .container import Container, ensure_collection, load_config


class Mediator(Container, collections.MutableMapping):
    """Models mediator."""

    def __init__(self, cfg, initialize=True):
        """Constructor setting configuration and task manager.

        :param cfg: Configuration or a file path from which to read
          configuration.
        :param initialize: Whether to initialize problem, or to stop
          after loading mediator configuration. Default is `True`.
        :type cfg: mapping or :py:class:`str`
        :type initialize: bool
        """
        # Load configuration
        loaded_cfg = cfg if isinstance(cfg, Config) else Config(cfg)

        #: Data-sources mapping.
        self.data_sources = collections.OrderedDict()

        #: Geographic configuration.
        self.geo_cfg = None
        #: Geographic data-source configuration.
        self.geo_src = None

        #: Component-managers mapping.
        self.component_managers = None

        #: Optimizer.
        self.optimizer = None

        #: Logger.
        self.log = logging.getLogger(loaded_cfg['project_name'])

        # Define as container without parent
        super(Mediator, self).__init__(self, 'mediator', cfg=loaded_cfg)

        if initialize:
            # Initialize
            self.initialize()

    def initialize(self):
        """Initialize mediator."""
        # Set-up logger
        _init_logger(self.log, self.cfg)

        if not self.cfg.get('no_verbose'):
            self.log.info('*** INITIALIZING MEDIATOR FOR {} ***'.format(
                self.cfg.get('project_name')))

        # Inject geography in mediator as data source
        self._init_geo()

        # Inject all components in mediator
        self._init_component_managers()

        # Inject optimizer
        self._init_optimizer()

    def add_data_source(self, src_vars, parent=None, isgeo=False,
                        **kwargs):
        """ Add single or multiple data source depending on whether
        :py:obj:`src_dict` has keys.

        :param src_vars: Mapping with multiple
          (source name, variable_names collection)
          (key, value) pairs, sequence of source names, source name.
        :param parent: Container for which to load the source.
          Default is `None`.
        :param isgeo: Whether data source is :py:class`.geo.GeoDataSourceBase`.
          Default is `False`.
        :type src_vars: Mutable mapping, collection or string.
        :type container: :py:class:`.container.Container`
        :type isgeo: bool

        :returns: Data source.
        :rtype: :py:class:`.data_source.DataSourceBase`

        .. seealso:: :py:meth:`.actuator_base.ActuatorBase.add_data_sources`
        """
        if ((not isinstance(src_vars, str)) and
            isinstance(src_vars, collections.Collection) and
                (len(src_vars) > 1)):
            data_src = self.med.add_multi_data_source(
                src_vars, parent=parent, isgeo=isgeo, **kwargs)
        else:
            if isinstance(src_vars, collections.Mapping):
                src_name, variable_names = src_vars.copy().popitem()
            else:
                # Try to get variables from keyword arguments,
                # otherwise, leave None
                variable_names = kwargs.pop('variable_names', None)
                src_name = str(*ensure_collection(src_vars))
            data_src = self.med.add_single_data_source(
                src_name, variable_names=variable_names, parent=parent,
                **kwargs)

        return data_src

    def add_single_data_source(self, name, variable_names=None, parent=None,
                               **kwargs):
        """Initialize a data source, inject to mediator,
        and return it as well.

        :param name: Data source name.
        :param variable_names: Data source variables. Default is `None`,
          in which case variables should be defined after construction
          by data source or by user.
        :param parent: Container for which to add data source.
          Default is `None`.
        :type name: str
        :type variable_names: (collection of) :py:class:`str`
        :type parent: :py:class:`.container.Container`

        :returns: (Multiple) data source.
        :rtype: :py:class:`.data_source.DataSourceBase`

        .. seealso:: :py:meth:`add_data_source`
        """
        # Verify that data source not already added by other containers
        if name not in self.data_sources:
            # Add data source configuration
            cfg_src = load_config(self, name, parent)

            if cfg_src is None:
                # Raise exception if configuration not found
                raise ValueError('No {} data source injected: no '
                                 'configuration found'.format(name))

            # Import data-source module
            mod = import_module_from_cfg(cfg_src, name=name)

            if mod is None:
                raise ValueError('Could not import module for '
                                 '{} data source'.format(name))

            # Create data source and inject it to mediator
            self.data_sources[name] = mod.DataSource(
                self, name, cfg=cfg_src, variable_names=variable_names,
                **kwargs)

            if not self.cfg.get('no_verbose'):
                self.log.info(
                    '{} data source injected to mediator'.format(name))
        else:
            # Add variable names to existing data source, if needed
            if variable_names is not None:
                self.data_sources[name].update_variables(variable_names)

        return self.data_sources[name]

    def add_multi_data_source(self, src_vars, parent=None, isgeo=False):
        """Initialize multiple data source, inject to mediator,
        and return it as well.

        :param src_vars: Mapping with multiple
          (source name, variable_names list)
          (key, value) pairs, sequence of source names..
        :param parent: Container for which to add data source.
          Default is `None`.
        :param isgeo: Whether data source is :py:class`.geo.GeoDataSourceBase`.
          Default is `False`.
        :type src_vars: mapping, or collection.
        :type parent: :py:class:`.container.Container`
        :type isgeo: bool

        :returns: Multiple data source.
        :rtype: :py:class:`.data_source.MultiDataSource` or
          :py:class:`.data_source.MultiGeoDataSource`

        .. seealso:: :py:meth:`add_data_source`,
          :py:meth:`add_single_data_source`
        """
        if not isinstance(src_vars, collections.Mapping):
            # If a collection of source names is given, transform it
            # to a mapping from source names to None (variable_names)
            src_vars = {src_name: None for src_name in src_vars}

        data_sources = collections.OrderedDict()
        for src_name, variable_names in src_vars.items():
            # Add data source to mediator
            self.add_single_data_source(
                src_name, variable_names=variable_names, parent=parent)

            # Add data source to multi-data source dictionary
            data_sources[src_name] = self.data_sources[src_name]

        # Verify that multi data source not already added by other containers
        multi_src_name = MultiDataSource.get_name(data_sources)
        if multi_src_name not in self.data_sources:
            # Create multiple data source from data sources dictionary
            multi_data_src = (MultiGeoDataSource(self, data_sources) if isgeo
                              else MultiDataSource(self, data_sources))

            # Inject multiple data source to mediator
            self.data_sources[multi_src_name] = multi_data_src
        else:
            # Get existing multiple data source
            multi_data_src = self.data_sources[multi_src_name]

            # Update multiple data source with potential new data sources
            multi_data_src.update_data_sources(data_sources)

        return multi_data_src

    def _init_geo(self, **kwargs):
        """Initialize geographic data source(s).

        .. note:: Only data sources associated to areas present in
          the 'component_managers_per_area' entry of the mediator configuration
          are added.
        """
        self.geo_cfg = load_config(self, 'geo')
        if self.geo_cfg is not None:
            # Add data sources for areas required by components
            src_names = set([self.geo_cfg['data'][area] for area in self.cfg[
                'component_managers_per_area']])
            self.add_data_source(src_names, isgeo=True)

            # Assign convenience member pointing to (multiple) geo data source
            src_names = ensure_collection(src_names)
            multi_src_name = (MultiDataSource.get_name(src_names)
                              if len(src_names) > 1 else src_names[0])
            self.geo_src = self.data_sources[multi_src_name]
        else:
            self.log.warning('No geographic data source provided: skipping')

    def _init_component_managers(self, **kwargs):
        """Initialize components."""
        # Get area-component managers mapping
        area_component_managers = self.cfg.get('component_managers_per_area')

        if area_component_managers is not None:
            # Initialize component-managers mapping
            self.component_managers = collections.OrderedDict()

            # Loop over area-component managers pairs
            for area, cfg_component_managers in (
                    area_component_managers.items()):
                if not self.cfg.get('no_verbose'):
                    scmp = ', '.join(cfg_component_managers.keys())
                    self.log.info(
                        'Injecting {} component managers for {} to '
                        'mediator'.format(scmp, area))

                # Loop over component manager-result managers pairs
                for component_mng_name, result_mng_names in (
                        cfg_component_managers.items()):
                    # Add component manager
                    self.component_managers[component_mng_name] = (
                        ComponentManager(self, component_mng_name, area=area,
                                         result_mng_names=result_mng_names))
        else:
            self.log.warning('No component manager provided: skipping')

    def _init_optimizer(self, **kwargs):
        """Initialize optimizer to associate to the given mediator."""
        # Add optimizer configuration
        opt_name = self.cfg.get('optimizer')
        if opt_name is not None:
            name = self.cfg['optimizer']
            cfg_opt = load_config(self, name)

            # Import data-source module
            mod = import_module_from_cfg(cfg_opt, name=name)

            # Add data source to mediator
            self.optimizer = mod.Optimizer(self, cfg=cfg_opt, **kwargs)

            if not self.cfg.get('no_verbose'):
                self.log.info('{} injected to mediator'.format(
                    self.optimizer.name))
        else:
            self.log.warning('No optimizer provided: skipping')

    def get_component_names_per_variable_for_source(
            self, src_name, variable_names=None, component_names=None,
            **kwargs):
        """Get component names per variable for data source.

        :param src_name: Data-source name.
        :param variable_names: Variable names.
          Default is `None`, in which case all variables in
          :py:attr:`variable_names` are returned.
        :param component_names: Component names.
          Default is `None`, in which case all mediator components
          that have :py:obj:`self` as data source are returned.
        :type src_name: str
        :type variable_names: (collection of) :py:class:`str`
        :type component_names: (collection of) :py:class:`str`

        :returns: Component names.
        :rtype: set
        """
        # Ensure collection
        component_names = ensure_collection(component_names, set)

        # Get set of component managers
        if component_names is None:
            # From mediator component managers
            component_managers = self.component_managers
        else:
            # From mediator component managers whose component names are in
            # the given component names
            component_managers = collections.OrderedDict()
            for name, component_mng in self.component_managers.items():
                if component_mng.component_name in component_names:
                    component_managers[name] = component_mng

        d = collections.OrderedDict()
        for component_mng in component_managers.values():
            if src_name in component_mng.data_sources:
                if variable_names is None:
                    # Add variables associated to component results
                    for result_mng in component_mng.result_managers.values():
                        d.setdefault(result_mng.result_name, set()).add(
                            component_mng.component_name)
                else:
                    # Add all variables for component
                    for variable_name in variable_names:
                        d.setdefault(variable_name, set()).add(
                            component_mng.component_name)

        return d

    def __getitem__(self, component_mng_name):
        """Get component from :py:attr:`components`.

        :param component_mng_name: Component-manager name.
        :type component_mng_name: str

        :returns: Component manager.
        :rtype: :py:class:`.component.ComponentManager`
        """
        return self.component_managers[component_mng_name]

    def get(self, component_mng_name, default=None):
        """Get component from :py:attr`data`.

        :param component_mng_name: Component-manager name.
        :param default: Default value. Default is `None`.
        :type component_mng_name: str
        :type default: :py:class:`.component.ComponentManager`

        :returns: component.
        :rtype: :py:class:`.component.ComponentManager`
        """
        return self.component_managers.get(component_mng_name, default)

    def __setitem__(self, component_mng_name, component_mng):
        """Set component in :py:attr:`data`.

        :param component_mng_name: Component-manager name.
        :param component_mng: Component manager to set.
        :type component_mng_name: str
        :type component_mng: :py:class:`.component.ComponentManager`
        """
        self.component_managers[component_mng_name] = component_mng

    def __contains__(self, component_mng_name):
        """Test if component manager in :py:attr:`component_managers`.

        :param component_mng_name: component name.
        :type component_mng_name: str
        """
        return component_mng_name in self.component_managers

    def __delitem__(self, component_mng_name):
        """Remove component manager from :py:attr:`component_managers`.

        :param component_mng_name: Component-manager name.
        :type component_mng_name: str
        """
        del self.component_managers[component_mng_name]

    def __iter__(self):
        """Iterate :py:attr:`component_managers` mapping."""
        return iter(self.component_managers)

    def __len__(self):
        """Number of component managers."""
        return len(self.component_managers)


def _init_logger(log, cfg):
    """Initialize logger.

    :param log: Logger.
    :param cfg: Logger configuration.
    :type log: :py:class:`logging.Logger`
    :type cfg: mapping
    """
    log_path = cfg.get('log_path')
    log_level = cfg.get('log_level', 'INFO')
    log_fmt0 = ('%(asctime)s/%(name)s/%(module)s.%(funcName)s:%(lineno)d/'
                '%(levelname)s: %(message)s')
    log_fmt = cfg.get('log_fmt', log_fmt0)
    capture_warnings = cfg.get('capture_warnings', True)

    # Configure logger
    log.setLevel(log_level)

    # Create file or stream handler
    if log_path is not None:
        # If log_path given, log to file instead of stream
        log_path = os.path.join(*ensure_collection(log_path))
        msg = ('Setting loggging to {}. '
               'Open it for further information'.format(log_path))
        warn(msg)
        # Make sure that log-file directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        hdlr = logging.FileHandler(log_path, mode='a')
    else:
        hdlr = logging.StreamHandler()

    # Add formatter and set level
    formatter = logging.Formatter(log_fmt)
    hdlr.setFormatter(formatter)
    hdlr.setLevel(log_level)

    # Add handler to root logger if needed
    if not log.hasHandlers():
        log.addHandler(hdlr)

    # Add handler to warning logger if needed
    if capture_warnings:
        logging.captureWarnings(capture_warnings)
        warn_log = logging.getLogger('py.warnings')
        if not warn_log.hasHandlers():
            warn_log.addHandler(hdlr)

    # Add handler to matplotlib logger if needed
    mpl_log = logging.getLogger('matplotlib')
    if not mpl_log.hasHandlers():
        mpl_log.addHandler(hdlr)
