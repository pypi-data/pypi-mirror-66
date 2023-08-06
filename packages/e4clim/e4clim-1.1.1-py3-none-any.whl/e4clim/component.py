"""Component and result managers base definitions."""
from collections import MutableMapping, OrderedDict
from .container import Container, ensure_collection, load_config
from .data_source import DataSourceBase, MultiDataSource
from .actuator_base import add_actuator


class ResultManager(DataSourceBase):
    """Manager for prediction results or output variables associated with a
    component."""

    def __init__(self, component_mng, name, cfg=None, **kwargs):
        """Constructor.

        :param component_mng: Component manager to which variable is
          associated.
        :param name: Result manager name.
        :param cfg: Result manager configuration. Default is `None`.
        :type component_mng: :py:class:`ComponentManager`
        :type name: str
        :type cfg: mapping
        """
        #: Component manager of result manager
        self.component_mng = component_mng

        #: Actuators.
        self.actuators = OrderedDict()

        #: Data sources.
        self.data_sources = OrderedDict()

        #: Features for each stage. Used in feature-extraction cases.
        self.feature = OrderedDict()

        #: Stage to extractor mapping.
        self.extractor = OrderedDict()

        #: Prediction result data source.
        self.prediction = None

        #: Result data source. Either :py:attr:`prediction`
        #:  or :py:attr:`feature['output']`.
        self.result = None

        # Initialize as container with component manager as parent
        super(ResultManager, self).__init__(
            med=self.component_mng.med, name=name, cfg=cfg,
            parent=component_mng, **kwargs)

        #: Result name.
        self.result_name = self.cfg.get('result_name') or self.name

        # Initialize actuators from configuration
        for actuator_name in self.cfg:
            actuator = add_actuator(
                self, actuator_name=actuator_name, **kwargs)

            # Add given actuator as attribute
            setattr(self, actuator_name, actuator)

            # Reference actuator in actuators set
            self.actuators[actuator_name] = actuator

        # Add data sources required by result manager (from all of its
        # actuators)
        for actuator in self.actuators.values():
            if actuator.data_sources is not None:
                for data_src in actuator.data_sources.values():
                    # Add as single data source
                    self.data_sources.update({data_src.name: data_src})

                    # Add as single data sources from multiple data source
                    if isinstance(data_src, MultiDataSource):
                        self.data_sources.update({
                            single_data_src.name: single_data_src
                            for single_data_src in
                            data_src.data_sources.values()})

        # Initialize extractors
        self._init_extractors(**kwargs)

        # Initialize data attributes
        self._init_data_attributes(**kwargs)

    def _init_extractors(self, **kwargs):
        """Initialize extractors."""
        # Add output extractor
        self.extractor['output'] = self.output_extractor

        if hasattr(self, 'feature_extractor'):
            # Add feature extractors for all stages
            for stage in 'fit', 'predict':
                self.extractor[stage] = self.feature_extractor

    def _init_data_attributes(self, **kwargs):
        """Initialize data attributes.

        .. warning:: :py:meth:`_init_extractors` must be called before.
        """
        # Initialize output-feature data source
        self.feature['output'] = Feature(self, stage='output', **kwargs)

        if hasattr(self, 'estimator'):
            # Initialize prediction data source
            self.prediction = Prediction(self, **kwargs)

            # Assign prediction to result
            self.result = self.prediction
        else:
            # Assign output feature to result
            self.result = self.feature['output']

        # Plug result methods to output variable
        self.update_variables(self.result.variable_names, **kwargs)
        self.data = self.result.data
        self.get_data_postfix = self.result.get_data_postfix
        self.get_data_path = self.result.get_data_path

        # Initialize features, associated with inputs
        if hasattr(self, 'feature_extractor'):
            for stage in self.feature_extractor.stages:
                self.feature[stage] = Feature(self, stage=stage, **kwargs)

    def extract(self, stage, **kwargs):
        """Extract or read feature from input data,
        store it in the :py:attr:`feature` member, and save it to file.

        :param stage: Modeling stage: `'fit'`, `'predict'` or `'output'`.
        :type stage: str
        """
        extractor = self.extractor[stage]
        if extractor.task_mng.get('extract__' + stage):
            # Extract feature
            # Get input data source
            data_src = extractor.data_sources[stage]
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Extracting {} feature to {} {} from {}'.format(
                        self.component_mng.name, stage, self.name,
                        data_src.name))

            # Extract feature from the input data
            self.feature[stage].update(
                extractor.transform(data_src=data_src, stage=stage, **kwargs))

            # Write all variables of feature
            if extractor.task_mng.get('write__' + stage):
                self.feature[stage].write(**kwargs)

            # Update task manager
            extractor.task_mng['extract__' + stage] = False
        else:
            # Read feature for variable
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    '{} feature to {} {} already extracted'.format(
                        self.component_mng.name, stage, self.name))
            self.feature[stage].read(**kwargs)

    def fit(self, **kwargs):
        """Fit estimator.

        .. note:: Input and output data for the fitting are read from file.
          They should thus be extracted before.
        """
        # Read or fit
        stage = 'fit'
        if hasattr(self, 'estimator'):
            if self.estimator.task_mng.get(stage):
                # Get input feature
                self.extract(stage, **kwargs)

                # Get output data
                self.extract('output', **kwargs)

                # Fit estimator
                if not self.cfg.get('no_verbose'):
                    self.log.info('Fitting {} {} estimator'.format(
                        self.component_mng.name, self.name))
                self.estimator.fit(self.feature[stage], self.feature['output'],
                                   **kwargs)

                # Save the fitted estimator
                self.estimator.write(**kwargs)

                # Update task managern
                self.estimator.task_mng[stage] = False
            else:
                # Load the estimator coefficients from file
                if not self.cfg.get('no_verbose'):
                    self.log.info('{} {} estimator already fitted'.format(
                        self.component_mng.name, self.name))
                self.estimator.read(**kwargs)
        else:
            if not self.cfg.get('no_verbose'):
                self.log.info('No estimator provided: skipping.')

    def predict(self, variable_names=None, **kwargs):
        """Predict and store result to :py:attr:`prediction` member.

        :param variable_names: Variable names. Default is `None`.
        :type variable_names: (collection of) :py:class:`str`

        .. note:: Input data for the prediction is read from file.
          It should thus be extracted before.
        """
        stage = 'predict'
        if hasattr(self, 'estimator'):
            if self.estimator.task_mng.get(stage):
                # Get estimator
                self.fit(**kwargs)

                # Get feature to predict
                self.extract(stage, **kwargs)

                # Apply
                if not self.cfg.get('no_verbose'):
                    self.log.info('Predicting {} {}'.format(
                        self.component_mng.name, self.name))
                self.prediction.update(self.estimator.predict(
                    self.feature[stage], **kwargs))

                # Save
                # Warning: input data to fit estimator will be forgotten
                self.prediction.write(variable_names=self.name, **kwargs)

                # Update task manager
                self.estimator.task_mng[stage] = False
            else:
                # Read prediction
                if not self.cfg.get('no_verbose'):
                    self.log.info('{} {} already predicted'.format(
                        self.component_mng.name, self.name))
                self.prediction.read(variable_names=self.name, **kwargs)
        else:
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'No {} {} estimator provided: skipping.'.format(
                        self.component_mng.name, self.name))

    def get_data(self, variable_names=None, **kwargs):
        """Get output from prediction if :py:attr:`estimator` is not `None`,
        or directly from (extracted) output data source, and store it in
        :py:attr:`result`.

        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr`variable_names` are downloaded.
        :type variable_names: (collection of) :py:class:`str`

        :returns: Dataset :py:attr:`data`.
        :rtype: mapping
        """
        if hasattr(self, 'estimator'):
            # Predict
            self.predict(**kwargs)
        else:
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'No {} {} estimator provided: directly extracting '
                    'output data'.format(self.component_mng.name, self.name))
            # Get data
            self.extract('output', **kwargs)

        return self.data


class ComponentManager(Container, MutableMapping):
    """Component manager."""

    def __init__(self, med, name, cfg=None, result_mng_names=None,
                 area=None, **kwargs):
        """Initialize component manager attached to mediator.

        :param med: Mediator.
        :param name: Component-manager name.
        :param cfg: Component-manager configuration.
          Default is `None`, in which case it is loaded by
          :py:func:`.container.load_config`.
        :param result_mng_names: Result-manager name(s)
          to estimate for component.
        :param area: Area to which the component manager is assigned.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        :type result_mng_names: (collection of) :py:class:`str`
        :type area: str
        """
        # Load component-manager configuration
        loaded_cfg = (cfg or load_config(med, name))

        #: Result managers of component manager.
        self.result_managers = OrderedDict()

        #: Component-manager data sources.
        #: Union of data sources from all result managers.
        self.data_sources = OrderedDict()

        # Initialize as container with mediator as parent
        super(ComponentManager, self).__init__(
            med, name, cfg=loaded_cfg, parent=med, **kwargs)

        #: Component name.
        self.component_name = self.cfg.get('component_name') or self.name

        #: Covered area.
        self.area = area

        #: Places in area.
        self.place_names = None
        if area and getattr(self.med, 'geo_src'):
            self.place_names = list(self.med.geo_src.area_places_sources[area])

        # Add result managers
        result_mng_names = ensure_collection(result_mng_names)
        for result_mng_name in result_mng_names:
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Injecting {} result manager in {} component '
                    'manager'.format(result_mng_name, self.name))
            self.result_managers[result_mng_name] = ResultManager(
                self, result_mng_name, cfg=self.cfg[result_mng_name])

        # Add data sources required by component manager (from all of its
        # result managers)
        for result_mng in self.result_managers.values():
            self.data_sources.update(result_mng.data_sources)

    def __getitem__(self, result_mng_name):
        """Get result manager from :py:attr:`result_managers`.

        :param result_mng_name: Result-manager name.
        :type result_mng_name: str

        :returns: Result manager.
        :rtype: :py:class:`ResultManager`
        """
        return self.result_managers[result_mng_name]

    def get(self, result_mng_name, default=None):
        """Get result manager from :py:attr`data`.

        :param result_mng_name: Result-manager name.
        :param default: Default value. Default is `None`.
        :type result_mng_name: str
        :type default: :py:class:`ResultManager`

        :returns: Result manager.
        :rtype: :py:class:`ResultManager`
        """
        return self.result_managers.get(result_mng_name, default)

    def __setitem__(self, result_mng_name, result_mng):
        """Set result manager in :py:attr:`data`.

        :param result_mng_name: Result-manager name.
        :param result_mng: Result manager to set.
        :type result_mng_name: str
        :type result_mng: :py:class:`ResultManager`
        """
        self.result_managers[result_mng_name] = result_mng

    def __contains__(self, result_mng_name):
        """Test if result manager in result managers.

        :param result_mng_name: Result-manager name.
        :type result_mng_name: str
        """
        return result_mng_name in self.result_managers

    def __delitem__(self, result_mng_name):
        """Remove result manager from :py:attr:`result_managers`.

        :param result_mng_name: Result-manager name.
        :type result_mng_name: str
        """
        del self.result_managers[result_mng_name]

    def __iter__(self):
        """Iterate :py:attr:`result_managers` mapping."""
        return iter(self.result_managers)

    def __len__(self):
        """Number of result managers."""
        return len(self.result_managers)


class ResultDataSourceBase(DataSourceBase):
    """Base result data."""

    def __init__(self, result_mng, name=None, variable_names=None, **kwargs):
        """Initialize feature as data source.

        :param result_mng: Result manager to which data is associated.
        :param name: Data name.
        :param variable_names: Name(s) of variable(s) composing dataset.
          Default is `None`.
        :type result_mng: :py:class:`.component.ResultManager`
        :type name: str
        :type variable_names: (collection of) :py:class:`str`
        """
        # Attach component manager and result manager
        #: Data-source result manager.
        self.result_mng = result_mng
        #: Component manager.
        self.component_mng = self.result_mng.component_mng

        kwargs.update({
            'med': self.component_mng.med, 'name': name,
            'variable_names': variable_names, 'cfg': self.result_mng.cfg,
            'task_names': None})
        super(ResultDataSourceBase, self).__init__(**kwargs)

    def get_data_dir(self, makedirs=True, **kwargs):
        """Get path to data directory.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Data directory path.
        :rtype: str
        """
        return self.med.cfg.get_project_data_directory(
            self.component_mng, makedirs=makedirs)


class Feature(ResultDataSourceBase):
    """Feature data source."""

    def __init__(self, result_mng, stage, **kwargs):
        """Initialize feature as data source.

        :param result_mng: Result manager to which data is associated.
        :param stage: Modeling stage: `'fit'` or `'predict'`.
        :type result_mng: str
        :type stage: str
        """
        #: Data-source estimation-stage.
        self.stage = stage

        #: Extractor.
        self.extractor = result_mng.extractor[stage]

        # Variables from extractors or as result_mng
        variable_names = (self.extractor.variable_names or
                          set([result_mng.result_name]))

        # Build result-manager data source with extractor variables
        name = '{}_{}'.format(result_mng.component_mng.name, self.stage)
        super(Feature, self).__init__(
            result_mng=result_mng, name=name,
            task_names=None, variable_names=variable_names, **kwargs)

        # Plug get_data_path method from extractor if possible
        if hasattr(self.extractor, 'get_data_path'):
            self.get_data_path = self.extractor.get_data_path

    def get_data_postfix(self, **kwargs):
        """Get feature postfix (overwrite :py:class:`DataSourceBase`
        implementation).

        :returns: Postfix.
        :rtype: str
        """
        # Get input data postfix
        data_src = self.extractor.data_sources[self.stage]
        feature_postfix = data_src.get_data_postfix(
            with_src_name=True, **kwargs)

        # Add modifier postfix
        if (hasattr(self.result_mng, 'modifier')
                and (self.stage in ['predict', 'output'])):
            feature_postfix += (self.result_mng.modifier.
                                get_extractor_postfix(**kwargs))

        # Add feature postfix
        feature_postfix += self.extractor.get_extractor_postfix(**kwargs)

        return feature_postfix

    def get_data_path(self, *args, **kwargs):
        """Get data path from base or from original data source if no
        extraction is performed."""
        if self.extractor.no_extraction:
            return self.extractor.data_sources[self.stage].get_data_path(
                *args, external=True, **kwargs)
        else:
            return super(Feature, self).get_data_path(*args, **kwargs)


class Prediction(ResultDataSourceBase):
    """Prediction data source."""

    def __init__(self, result_mng, **kwargs):
        """Initialize prediction as data source.

        :param result_mng: Result manager to which data is associated.
        :type result_mng: str
        """
        # Build result-manager data source
        name = '{}_prediction'.format(result_mng.component_mng.name)
        super(Prediction, self).__init__(
            result_mng=result_mng, name=name,
            variable_names=result_mng.result_name, task_names=None, **kwargs)

    def get_data_postfix(self, **kwargs):
        """Get prediction postfix.

        :returns: Postfix.
        :rtype: str
        """
        return self.result_mng.estimator.get_fit_postfix(**kwargs)


class DataSourceWithComponentsMixin():
    """Add components management to data source loader."""

    def get_component_names_per_variable(
            self, variable_names=None, component_names=None, **kwargs):
        """Get set of component names from argument or from all mediator
        components that have :py:obj:`self` as data source and sort them
        by variable.

        :param variable_names: Variable names.
          Default is `None`, in which case all variables in
          :py:attr:`variable_names` are returned.
        :param component_names: Component names.
          Default is `None`, in which case all mediator components
          that have :py:obj:`self` as data source are returned.
        :type variable_names: (collection of) :py:class:`str`
        :type component_names: (collection of) :py:class:`str`

        :returns: Component names.
        :type component_names: collection of :py:class:`str`
        """
        # Ensure collection for given/data-source variable names
        variable_names = (ensure_collection(variable_names, set)
                          or self.variable_names)

        # Get variable-component names mapping
        return self.med.get_component_names_per_variable_for_source(
            self.name, variable_names, component_names, **kwargs)

    def finalize_array(self, da, variable_name, **kwargs):
        """Finalize array adding/converting units if possible,
          transposing, naming. Used by APIs.

        :param da: Data array.
        :param variable_name: Variable name.
        :type da: :py:class:`xarray.DataArray`
        :type variable_name: str
        """
        # Convert units if possible
        try:
            da = da * float(self.cfg['unit_conversions'][variable_name])
        except (KeyError, TypeError):
            pass

        # Add units if possible
        try:
            da.attrs['units'] = str(self.cfg['units'][variable_name])
        except KeyError:
            da.attrs['units'] = 'Unknown'

        # Transpose
        da = da.transpose('time', 'component', 'region')

        # Name array as variable
        da.name = variable_name

        return da


def finalize_dataset(func):
    """"Decorator to finalize arrays in dataset returned by
    :py:meth:`..data_source.DataSourceLoaderBase.load`.

    :param func: Function to be decorated.
    :type func: function

    .. seealso:: :py:meth:`finalize_array`
    """

    # Define decorating function
    def inner(self, variable_component_names=None, **kwargs):
        # Call function to get dataset
        ds = func(self, variable_component_names, **kwargs)

        # Finalize arrays for all variables
        for variable_name, da in ds.items():
            ds[variable_name] = self.finalize_array(
                da, variable_name, **kwargs)

        return ds

    return inner


def parse_variable_component_args(func):
    """"Decorator to parse variable_names and/or variable_component_names
    arguments for :py:meth:`..data_source.DataSourceLoaderBase.download`
    and :py:meth:`..data_source.DataSourceLoaderBase.load`.

    :param func: Function to be decorated.
    :type func: function
    """

    # Define decorating function
    def inner(self, variable_names=None, component_names=None,
              variable_component_names=None, **kwargs):
        if variable_component_names is None:
            # Get variable-component names mapping
            variable_component_names = self.get_component_names_per_variable(
                variable_names, component_names, **kwargs)
        else:
            # Ensure component names as collections
            for variable_name, component_names in (
                    variable_component_names.items()):
                variable_component_names[
                    variable_name] = ensure_collection(component_names, set)

        # Call function and return
        return func(self, variable_component_names, **kwargs)

    return inner


def download_to_compute_capacity_factor(func):
    """Decorator to handle capacity factor from capacity and generation.
    in :py:meth:`..data_source.DataSourceLoaderBase.download`
    and :py:meth:`..data_source.DataSourceLoaderBase.load`.

    :param func: Function to be decorated.
    :type func: function
    """

    # Define decorating function
    def inner(self, variable_component_names=None, **kwargs):
        # Add capacity factor to variable to load names
        variable_component_to_load_names = add_capacity_factor(
            variable_component_names, **kwargs)

        # Call function and return
        return func(self, variable_component_to_load_names, **kwargs)

    return inner


def compute_capacity_factor(func):
    """Decorator to handle capacity factor from capacity and generation.
    in :py:meth:`..data_source.DataSourceLoaderBase.download`
    and :py:meth:`..data_source.DataSourceLoaderBase.load`.

    :param func: Function to be decorated.
    :type func: function
    """

    # Define decorating function
    def inner(self, variable_component_names=None, **kwargs):
        # Add capacity factor to variable to load names
        variable_component_to_load_names = add_capacity_factor(
            variable_component_names, **kwargs)

        # Call function
        ds = func(self, variable_component_to_load_names, **kwargs)

        # Get capacity factor
        variable_name = 'capacity_factor'
        if variable_name in variable_component_names:
            # Get capacity factor
            da = self._get_capacity_factor(ds, **kwargs)

            # Add variable to dataset
            ds[variable_name] = self.finalize_array(
                da, variable_name, **kwargs)

        # Select variables
        ds_sel = {}
        for variable_name in variable_component_names:
            ds_sel[variable_name] = ds[variable_name]

        return ds_sel

    return inner


def add_capacity_factor(variable_component_names, **kwargs):
    """Add capacity factor to :py:obj:`variable_component_to_load_names`.

    :param variable_component_names: Names of components to load per
      variable.
    :type variable_component_names: mapping from :py:class:`str`
      to collection

    :returns: Names of components to load per variable with
      capacity factor added.
    :rtype: mapping from :py:class:`str` to collection
    """
    # Add capacity and generation to variables to load
    variable_name = 'capacity_factor'
    variable_component_to_load_names = variable_component_names.copy()
    if variable_name in variable_component_names:
        # Make sure that generation and capacity are loaded
        variable_component_to_load_names.update(
            {'generation': variable_component_names[variable_name],
             'capacity': variable_component_names[variable_name]})

        # Remove capacity factor from variables to load
        del variable_component_to_load_names['capacity_factor']

    return variable_component_to_load_names
