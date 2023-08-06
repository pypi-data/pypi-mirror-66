"""Optimization base definitions."""
from abc import ABC, abstractmethod
from .container import Container, load_config
from .data_source import DataSourceLoaderBase


class OptimizerBase(Container, ABC):
    """Optimizer abstract base class. Requires :py:meth:`solve` method to be
    implemented."""

    def __init__(self, med, name, cfg=None, **kwargs):
        """Build optimizer linked to mediator.

        :param med: Mediator.
        :param name: Optimizer name.
        :param cfg: Optimizer configuration.
          If `None`, call :py:meth:`.config._load_src_coonfig`.
          Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        # Load optimizer configuration
        loaded_cfg = cfg or load_config(self.med, self.name)

        # Initialize as container with mediator as parent
        super(OptimizerBase, self).__init__(
            med, name, cfg=loaded_cfg, parent=med, **kwargs)

        #: Input data source.
        self.input = None

        #: Solution data source.
        self.solution = SolutionBase(self, **kwargs)

    @abstractmethod
    def solve(self, *args, **kwargs):
        """Abstract method to solve optimization problem."""
        raise NotImplementedError


class InputBase(DataSourceLoaderBase):
    """Abstract optimization input class as data source with loader.
    Requires :py:meth:`load` method inherited from
    :py:class:`.data_source.DataSourceLoaderBase` to be implemented."""

    def __init__(self, optimizer, cfg=None, **kwargs):
        """Initialize input data source.

        :param optimizer: Optimizer.
        :param cfg: Input configuration. Default is `None`.
        :type optimizer: :py:class:`.optimization.OptimizerBase`
        :type cfg: mapping
        """
        self.optimizer = optimizer
        name = '{}_input'.format(self.optimizer.name)

        super(InputBase, self).__init__(
            self.optimizer.med, name, cfg=cfg, parent=self.optimizer, **kwargs)

    def get_data_postfix(self, **kwargs):
        """Get data postfix.

        :returns: Postfix.
        :rtype: str
        """
        return ''

    def get_data_dir(self, makedirs=True, **kwargs):
        """Get path to data directory.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Data directory path.
        :rtype: str
        """
        return self.med.cfg.get_project_data_directory(
            self.optimizer, subdirs='input', makedirs=makedirs)


class SolutionBase(DataSourceLoaderBase):
    """Optimization solution base class as data source."""

    def __init__(self, optimizer, cfg=None, **kwargs):
        """Initialize solution as data source.

        :param optimizer: Optimizer.
        :param cfg: Solution configuration. Default is `None`.
        :type optimizer: :py:class:`.optimization.OptimizerBase`
        :type cfg: mapping
        """
        self.optimizer = optimizer
        name = '{}_solution'.format(self.optimizer.name)

        super(SolutionBase, self).__init__(
            self.optimizer.med, name, cfg=cfg, parent=self.optimizer, **kwargs)

    def load(self, variable_names=None, **kwargs):
        """Load returning result from :py:meth:`OptimizerBase.solve`.

        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr`variables` are downloaded.
        :type variable_names: (collection of) :py:class:`str`
        """
        # Get input data
        self.optimizer.input.get_data(**kwargs)

        # Solve
        return self.optimizer.solve(variable_names=variable_names, **kwargs)

    def get_data_dir(self, makedirs=True, **kwargs):
        """Get path to data directory.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Data directory path.
        :rtype: str
        """
        return self.med.cfg.get_project_data_directory(
            self.optimizer, subdirs='solution', makedirs=makedirs)

    def get_data_postfix(self, **kwargs):
        """Default implementation of get optimization results postfix.

        :returns: Postfix.
        :rtype: str
        """
        return self.optimizer.input.get_data_postfix()
