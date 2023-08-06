"""Data-source base definitions."""
from abc import ABC, abstractmethod
import os
from collections import MutableMapping, OrderedDict
import functools
import xarray as xr
from .container import Container, ensure_collection


class DataSourceBase(Container, MutableMapping):
    """Base data-source class for APIs."""

    def __init__(self, med, name, cfg=None, variable_names=None,
                 task_names=None, parent=None, **kwargs):
        """Build data source linked to mediator.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :param variable_names: Name(s) of variable(s) composing dataset.
          Default is `None`.
        :param task_names: Names of potential tasks for container to perform.
          Default is `None`.
        :param parent: Parent container.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        :type variable_names: (collection of) :py:class:`str`
        :type task_names: set
        :type parent: :py:class:`.container.Container`
        """
        # Add read tasks per variable
        if variable_names is not None:
            variable_names = ensure_collection(variable_names, set)
            if task_names is None:
                task_names = set()
            for variable_name in variable_names:
                task_names.add('read__{}'.format(variable_name))
                task_names.add('write__{}'.format(variable_name))

        # Initialize as container
        parent = med if parent is None else parent
        super(DataSourceBase, self).__init__(
            med, name, cfg=cfg, task_names=task_names, parent=parent,
            **kwargs)

        #: Whether this is a gridded data source.
        #: By default, data source not gridded.
        self.gridded = False

        #: Data-source data.
        self.data = OrderedDict()

        #: Data-source variable names.
        self.variable_names = set()

        # Add set of variable names composing dataset
        if variable_names is not None:
            self.update_variables(variable_names)

        #: Variable to data-source mapping and variables list
        #: (for it to be useful, we need to assume that one and only one
        #: dataset is associated to a variable.
        #: This may be improved by adding information
        #: on the data source to variables names).
        self.var_data_sources = OrderedDict()

        # Update variable to data-source mapping,
        # for this single data source.
        for variable_name in self.variable_names:
            self.var_data_sources.setdefault(
                variable_name, {}).update({self.name: self})

    def update_variables(self, variable_names, **kwargs):
        """Add variable names to data source.

        :param variable_names: Name(s) of variable(s) to add.
        :type variable_names: (collection of) :py:class:`str`
        """
        variable_names = ensure_collection(variable_names, set)

        # Update variables set
        self.variable_names.update(variable_names)

        # Update tasks
        for variable_name in variable_names:
            task_name = 'read__{}'.format(variable_name)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})
            task_name = 'write__{}'.format(variable_name)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})

    def __getitem__(self, variable_name):
        """Get variable data from :py:attr:`data`.

        :param variable_name: Variable name.
        :type variable_name: str

        :returns: Variable.
        :rtype: :py:class:`xarray.DataArray`

        .. note: Calls `__getitem__` method from :py:class:`dict`.
        """
        return self.data[variable_name]

    def get(self, variable_name, default=None):
        """Get variable data from :py:attr`data`.

        :param variable_name: Variable name.
        :param default: Default value. Default is `None`.
        :type variable_name: str
        :type default: :py:class:`xarray.DataArray`

        :returns: Variable.
        :rtype: :py:class:`xarray.DataArray`

        .. note: Calls `get` method from :py:class:`dict`.
        """
        return self.data.get(variable_name, default)

    def __setitem__(self, variable_name, data):
        """Set item in :py:attr:`data`.

        :param variable_name: Variable name.
        :param data: Data of variable to set.
        :type variable_name: str
        :type data: :py:class:`xarray.DataArray`

        .. note: Calls `__setitem__` method from :py:class:`dict`.
        """
        self.data[variable_name] = data

    def __contains__(self, variable_name):
        """Test if variable in data source.

        :param variable_name: Variable name.
        :type variable_name: str
        """
        return variable_name in self.variable_names

    def __delitem__(self, variable_name):
        """Remove variable from :py:attr:`variables` set
        and from :py:attr:`data` mapping.

        :param variable_name: Variable name.
        :type variable_name: str
        """
        # Remove variable
        self.variable_names.remove(variable_name)
        # Remove data for variable
        del self.data[variable_name]

    def __iter__(self):
        """Iterate :py:attr:`data` mapping."""
        return iter(self.data)

    def __len__(self):
        """Number of variables."""
        return len(self.variable_names)

    def __str__(self):
        """Get dataset as string."""
        s = "<{} '{}'>\n".format(str(self.__class__)[8:-2], self.name)
        s += '{}'.format(self.data)

        return s

    def update(self, var_data):
        """Update data with given dataset.

        :param var_data: Dataset.
        :type var_data: Mapping of :py:class:`xarray.DataArray`
        """
        # Update variable list
        self.variable_names.update(var_data.keys())

        # Update data
        self.data.update(var_data)

    def copy_data(self, data_src, variable_name=None):
        """Copy data from another data source, e.g.
        of type :py:class:`Prediction` or :py:class:`Feature`.

        :param data_src: Data source to copy.
        :param variable_name: Name of a specific variable from which
          to copy data. Default is `None`
        :param data_src: :py:class:`.data_sources.`DataSourceBase`
        :param variable_name: str
        """
        if variable_name is not None:
            self.update({variable_name: data_src.get(variable_name)})
        else:
            self.update(data_src.data)

    def close(self, variable_names=None):
        """Close dataset.

        :param variable_names: Variable(s) to close. Default is `None`,
          in which case all variables are closed.
        :type variable_names: (collection of) :py:class:`str`
        """
        # Get variables list
        variable_names = (ensure_collection(variable_names, set) or
                          self.variable_names)

        # Close each variable separately
        for variable_name in variable_names:
            self.data[variable_name].close()

    def read(self, variable_names=None, **kwargs):
        """Read source dataset as dictionary of :py:class:`xarray.DataArray`.

        :param variable_names: Variable(s) to read. Default is `None`,
          in which case variables are read.
        :type variable_names: (collection of) :py:class:`str`
        """
        variable_names = (ensure_collection(variable_names, set) or
                          self.variable_names)

        if variable_names:
            # Update data source set of variables
            self.update_variables(variable_names)

            # Read each variable separately
            ds = {}
            for iv, variable_name in enumerate(variable_names):
                # Get data filepath
                filepath = '{}.nc'.format(self.get_data_path(
                    variable_name=variable_name, makedirs=False, **kwargs))
                if self.task_mng['read__{}'.format(variable_name)]:
                    if not self.cfg.get('no_verbose'):
                        self.log.info('Reading {} {} from {}'.format(
                            self.name, variable_name, filepath))
                    try:
                        # Try to load as dataarray
                        ds[variable_name] = xr.load_dataarray(filepath)
                    except ValueError:
                        # Or else load as dataset
                        ds[variable_name] = xr.load_dataset(filepath)

                    # Update task manager
                    self.task_mng['read__{}'.format(variable_name)] = False
                else:
                    # Skip
                    if not self.cfg.get('no_verbose'):
                        self.log.info(
                            '{} {} already read: skipping'.format(
                                self.name, variable_name))

            # Update dataset
            self.update(ds)
        else:
            self.log.warning('Empty variable-name collection given: no {} '
                             'data read'.format(self.name))

    def write(self, variable_names=None, **kwargs):
        """Write :py:class:`xarray.DataArray` of each variable in netcdf.

        :param variable_names: Variable(s) to write. Default is `None`,
          in which all variables are written.
        :type variable_names: (collection of) :py:class:`str`

        .. warning:: Exististing files are not overwritten.
          Only existing variables (groups) are.
        """
        variable_names = (ensure_collection(variable_names, set) or
                          self.variable_names)

        if variable_names:
            for iv, variable_name in enumerate(variable_names):
                filepath = '{}.nc'.format(self.get_data_path(
                    variable_name=variable_name, **kwargs))
                if self.task_mng.get('write__{}'.format(variable_name)):
                    if not self.cfg.get('no_verbose'):
                        self.log.info('Writing {} {} to {}'.format(
                            self.name, variable_name, filepath))
                    self.get(variable_name).to_netcdf(filepath, mode='w')

                    # Update task manager
                    self.task_mng['write__{}'.format(variable_name)] = False
                else:
                    # Skip
                    if not self.cfg.get('no_verbose'):
                        self.log.info(
                            '{} {} already written: skipping'.format(
                                self.name, variable_name))
        else:
            self.log.warning('Empty variable-name collection given: no {} '
                             'data written'.format(self.name))

    def get_postfix(self, **kwargs):
        """Return empty postfix string.

        returns: Postfix.
        rtype: str
        """
        return ''

    def get_data_postfix(self, with_src_name=False, **kwargs):
        """Get data-source postfix.
        A user-defined postfix may be defined in the `'postfix'`
        entry of the data source configuration.
        Otherwise, the standard postfix is used by calling
        :py:meth:`get_postfix`.
        The data-source name is prepended.

        :param with_src_name: Whether to prefix postfix with source name.
        :type with_src_name: bool

        :returns: Postfix.
        :rtype: str
        """
        # Get user-defined postfix or standard postfix
        postfix = self.cfg.get('postfix')
        postfix = (self.get_postfix(**kwargs) if postfix is None else
                   postfix)

        # Prepend data-source name
        if with_src_name:
            postfix = '_{}{}'.format(self.name, postfix)

        return postfix

    def get_data_path(self, variable_name=None, makedirs=True, **kwargs):
        """Get data-source filepath.

        :param variable_name: Data variable. Default is `None`.
        :param makedirs: Make directories if needed. Default is `True`.
        :type variable_name: str
        :type makedirs: bool

        :returns: Filepath.
        :rtype: str
        """
        # Variable string
        var_pf = '_{}'.format(variable_name) if variable_name else ''

        # Data-postfix string
        data_pf = self.get_data_postfix(
            variable_name=variable_name, **kwargs)

        # Filepath
        filename = '{}{}{}'.format(self.name, var_pf, data_pf)
        data_dir = self.get_data_dir(makedirs=makedirs, **kwargs)
        filepath = os.path.join(data_dir, filename)

        return filepath


class MultiDataSource(DataSourceBase, MutableMapping):
    def __init__(self, med, data_sources, task_names=set(),
                 default_tasks_value=True, **kwargs):
        """Build data source composed to multiple data sources
        and linked to mediator.

        :param med: Mediator.
        :param data_sources: Data sources dictionary.
        :param task_names: Names of potential tasks for container to perform.
          Default is `set()`.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none. Default is `True`.
        :type med: :py:class:`.mediator.Mediator`
        :type data_sources: :py:class:`dict` of :py:class:`DataSourceBase`
        :type task_names: set
        :type default_tasks_value: bool

        .. warn:: At the moment, a variable can only belong to one data source.
        """
        # Multiple data-source attributes specification
        cfg = None
        name = self.get_name(data_sources)

        # Initialize as data source
        super(MultiDataSource, self).__init__(
            med, name, cfg=cfg, task_names=task_names,
            default_tasks_value=default_tasks_value, **kwargs)

        #: Data sources composing multiple data source.
        self.data_sources = OrderedDict()

        # Update with data sources
        self.update_data_sources(data_sources)

    @staticmethod
    def get_name(data_sources):
        """Get class name from data_sources.

        :param data_sources: Data-sources list or data-source names list.
        :type data_sources: :py:class:`list` of :py:class:`DataSourceBase`
          or :py:class:`str`

        :returns: Multiple data-source name.
        :rtype: str
        """
        # Note: in principle, data_sources' keys correspond to name
        # attribute of each data_src
        try:
            name = '__'.join(data_src.name
                             for data_src in data_sources.values())
        except AttributeError:
            name = '__'.join(data_sources)

        return name

    def update_data_sources(self, data_sources):
        """Update :py:attr:`data_sources` and :py:attr:`variable_names`.

        :param data_sources: Data sources dictionary.
        :type data_sources: :py:class:`dict` of :py:class:`DataSourceBase`
        """
        for src_name, data_src in data_sources.items():
            # Update data sources
            self.data_sources.update({src_name: data_src})

            # Update variable names
            self.update_variables(data_src.variable_names)

            # Update variable to data-source mapping,
            # allowing for multiple data sources per variable
            for variable_name in data_src.variable_names:
                self.var_data_sources.setdefault(
                    variable_name, {}).update({src_name: data_src})

            # Check if gridded
            if data_src.gridded:
                self.gridded = True

            # Add data sources as children
            self.update_children(self.data_sources)

    def get_data_sources(self, variable_name):
        """Get single data source(s) containing variable.

        :param variable_name: Variable name.
        :type variable_name: str

        :returns: Data source(s) associated with variable.
        :rtype: (mapping of :py:class:`str` to) :py:class:`DataSourceBase`
        """
        data_sources = self.var_data_sources.get(variable_name)

        if len(data_sources) > 1:
            # Multiple data sources for this variable
            sel_data_sources = {src_name: data_src
                                for src_name, data_src in data_sources.items()}
        else:
            # Single data source
            sel_data_sources = list(data_sources.values())[0]

        return sel_data_sources

    def get(self, variable_name, default=None):
        """Get variable from data source containing variable.

        :param variable_name: Variable name.
        :param default: Default (mapping to) array(s). Default is `None`.
        :type variable_name: str
        :type default: (mapping of :py:class:`str` to)
          :py:class:`xarray.DataArray`

        :returns:

          * :py:class:`xarray.DataArray`, if a single data source is
            associated to variable,
          * Mapping from source names to variable-data.

        :rtype: (mapping of :py:class:`str` to) :py:class:`xarray.DataArray`

        .. seealso:: :py:meth:`get_data_sources`
        """
        # Data sources containing variable
        data_sources = self.get_data_sources(variable_name)

        if data_sources is not None:
            if isinstance(data_sources, DataSourceBase):
                # Single data source
                data = data_sources[variable_name]
            else:
                # Multiple data sources for this variable
                data = {src_name: data_src[variable_name]
                        for src_name, data_src in data_sources.items()}
        else:
            data = default

        return data

    def __getitem__(self, variable_name):
        """Get item from data source containing variable.

        :param variable_name: Variable name.
        :type variable_name: str

        :returns:

          * :py:class:`xarray.DataArray`, if a single data source is
            associated to variable,
          * Mapping from source names to variable-data.

        :rtype: (mapping of :py:class:`str` to) :py:class:`xarray.DataArray`
        """
        # Array(s) associated with variable
        data = self.get(variable_name)

        if data is None:
            # Variable not found
            raise KeyError(variable_name)

        return data

    def __iter__(self):
        """Iterate :py:attr:`data` mapping."""
        return iter(self.data_sources)

    def __str__(self):
        """Get dataset as string."""
        s = "<{} '{}'>\n".format(str(self.__class__)[8:-2], self.name)
        s += '\n'.join('{}\n{}'.format(str(data_src), str(data_src.data))
                       for data_src in self.data_sources.values())

        return s

    def __setitem__(self, variable_name, sources_data):
        """Set items in data sources containing variable.

        :param variable_name: Variable name.
        :param sources_data: Source name to variable-data-to-set mapping.
        :type variable_name: str
        :type data: mapping of :py:class:`str` to :py:class:`xarray.DataArray`
        """
        # Data source containing variable
        data_sources = self.var_data_sources[variable_name]

        # Set variable in data source
        for src_name, src_data in sources_data.items():
            data_sources[src_name][variable_name] = src_data

    def update(self, variable_data):
        """Update data with given dataset.

        :param variable_data: Dataset.
        :type variable_data: Mapping of :py:class:`xarray.DataArray`
        """
        for variable_name, sources_data in variable_data.items():
            # Mapping of single data source(s) containing variable
            data_sources = self.variable_data_sources[variable_name]

            # Update single data source
            for src_name, src_data in sources_data.items():
                data_sources[src_name].data.update(
                    {variable_name: src_data})

        # Update multiple data-source variables
        self.update_variables(variable_data.keys())

    def download(self, variable_names=None, **kwargs):
        """Download multiple data source calling :py:meth:`DataSourceBase.download`
        of each data source.

        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr:`variable_names` are downloaded.
        :type variable_names: (collection of) :py:class:`str`

        .. seealso:: :py:meth:`DataSourceBase.download`
        """
        for data_src in self.data_sources.values():
            if isinstance(data_src, DataSourceLoaderBase):
                # Download
                data_src.download(variable_names=variable_names, **kwargs)

    def manage_download(
            self, variable_names=None, **kwargs):
        """Manage multiple data-source download calling
        :py:meth:`DataSourceBase.manage_download` of each data source.

        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr`variable_names` are downloaded.
        :type variable_names: (collection of) :py:class:`str`

        .. seealso:: :py:meth:`DataSourceBase.manage_download`
        """
        for data_src in self.data_sources.values():
            if isinstance(data_src, DataSourceLoaderBase):
                data_src.manage_download(
                    variable_names=variable_names, **kwargs)

    def load(self, variable_names=None, **kwargs):
        """Load multiple data source calling :py:meth:`DataSourceBase.load`
        of each data source.

        :param variable_names: Names of variables to load.
          Default is `None`, in which case all variables in
          :py:attr:`variable_names` are loaded.
        :type variable_names: (collection of) :py:class:`str`

        .. seealso:: :py:meth:`DataSourceBase.load`
        """
        d = {}
        for data_src in self.data_sources.values():
            if isinstance(data_src, DataSourceLoaderBase):
                # Load
                d[data_src.name] = data_src.load(
                    variable_names=variable_names, **kwargs)

        return d

    def get_data(self, variable_names=None, **kwargs):
        """Load data from multiple data sources calling
        :py:meth:`DataSourceBase.get_data` of each data source.

        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr`variable_names` are downloaded.
        :type variable_names: (collection of) :py:class:`str`

        :returns: Dataset :py:attr:`data`.
        :rtype: mapping

        .. seealso:: :py:meth:`DataSourceBase.get_data`
        """
        for data_src in self.data_sources.values():
            if isinstance(data_src, DataSourceLoaderBase):
                # Get data for single source, transmitting keywords
                data_src.get_data(variable_names=variable_names, **kwargs)

        return self.data

    def get_mask(self, **kwargs):
        """Get mask for gridded single data sources calling
        :py:meth:`GriddedDataSourceBase.get_mask`.

        .. seealso:: :py:meth:`GriddedDataSourceBase.get_mask`
        """
        for data_src in self.data_sources.values():
            if data_src.gridded:
                # Get data for single source, transmitting keywords
                data_src.get_mask(**kwargs)

    def read(self, variable_names=None, **kwargs):
        """Read multiple data source.

        .. seealso:: :py:meth:`DataSourceBase.read`
        """
        for src_label, data_src in self.data_sources.items():
            data_src.read(variable_names=variable_names, **kwargs)

    def write(self, variable_names=None, **kwargs):
        """Write multiple data source.

        .. seealso:: :py:meth:`DataSourceBase.write`
        """
        for data_src in self.data_sources.values():
            data_src.write(variable_names=variable_names, **kwargs)

    def get_data_postfix(self, with_src_name=False, **kwargs):
        """Get multiple data-source postfix as sum of each single
        data-source postfix.

        :param with_src_name: Whether to prefix postfix with source name.
        :type with_src_name: bool

        :returns: Postfix.
        :rtype: str
        """
        postfix = ''.join(data_src.get_data_postfix(
            with_src_name=with_src_name, **kwargs)
            for data_src in self.data_sources.values())

        return postfix


class DataSourceLoaderBase(DataSourceBase, ABC):
    """Data-source loader base class. Requires :py:meth:`load` method
    to be implemented. Also includes a passing :py:meth:`download` method."""

    def __init__(self, med, name, cfg=None, variable_names=None, parent=None,
                 task_names=None, **kwargs):
        """Build data source with downloading and loading capabilities.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :param variable_names: List of variables composing dataset.
          Default is `None`.
        :param parent: Parent container.
        :param task_names: Names of potential tasks for container to perform.
          Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        :type variable_names: (collection of) :py:class:`str`
        :type parent: :py:class:`.container.Container`
        :type task_names: set
        """
        # Add download and load tasks per variable
        if variable_names is not None:
            variable_names = ensure_collection(variable_names, set)
            if task_names is None:
                task_names = set()
            for variable_name in variable_names:
                task_names.add('load__{}'.format(variable_name))
                task_names.add('download__{}'.format(variable_name))

        super(DataSourceLoaderBase, self).__init__(
            med, name, cfg=cfg, variable_names=variable_names, parent=parent,
            task_names=task_names, **kwargs)

    def update_variables(self, variable_names, **kwargs):
        """Add variables to data source.

        :param variable_names: (List of) name(s) of variable(s) to add.
        :type variable_names: (collection of) :py:class:`str`
        """
        variable_names = ensure_collection(variable_names, set)

        super(DataSourceLoaderBase, self).update_variables(
            variable_names, **kwargs)

        # Update tasks
        for variable_name in variable_names:
            task_name = 'download__{}'.format(variable_name)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})
            task_name = 'load__{}'.format(variable_name)
            if task_name not in self.task_mng:
                self.task_mng.update({task_name: True})

    @abstractmethod
    def load(self, variable_names=None, **kwargs):
        """Retrieve data from the input source and return an object."""
        raise NotImplementedError

    def download(self, variable_names=None, **kwargs):
        """Download data."""
        self.log.warning('{} download not implemented'.format(self.name))

    def get_data(self, variable_names=None, **kwargs):
        """Read or load data from a given source and store it in
        :py:attr:`data` member.

        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr`variable_names` are downloaded.
        :type variable_names: (collection of) :py:class:`str`

        :returns: Dataset :py:attr:`data`.
        :rtype: mapping
        """
        # Get list of variables to load and to read
        variable_names = (ensure_collection(variable_names, set) or
                          self.variable_names)
        variable_to_load_names = variable_names.copy()
        for variable_name in variable_names:
            if not self.task_mng.get('load__{}'.format(variable_name)):
                variable_to_load_names.discard(variable_name)
        variable_to_read_names = variable_names.difference(
            variable_to_load_names)

        if variable_to_load_names:
            # Download data if needed
            self.manage_download(
                variable_names=variable_to_load_names, **kwargs)

            if not self.cfg.get('no_verbose'):
                svar = ', '.join(str(variable_name)
                                 for variable_name in variable_to_load_names)
                self.log.info('Loading {} {}'.format(self.name, svar))

            # Load data
            data = self.load(
                variable_names=variable_to_load_names, **kwargs)
            self.update(data)

            # Write data (all components, in case more than one)
            self.write(variable_names=variable_to_load_names, **kwargs)

            # Update task manager with all loaded variables
            # (even the ones that were not requested)
            for variable_name in data:
                self.task_mng['load__{}'.format(variable_name)] = False

        if variable_to_read_names:
            # Read variables
            if not self.cfg.get('no_verbose'):
                svar = ', '.join(str(variable_name)
                                 for variable_name in variable_to_read_names)
                self.log.info(
                    '{} {} already loaded'.format(self.name, svar))
            self.read(variable_names=variable_to_read_names, **kwargs)

        return self.data

    def manage_download(self, variable_names=None, **kwargs):
        """Manage data download.

        :param variable_names: Names of variables to download.
          Default is `None`, in which case all variables in
          :py:attr`variable_names` are downloaded.
        :type variable_names: (collection of) :py:class:`str`
        """
        # Get list of variables to download
        variable_names = (ensure_collection(variable_names, set) or
                          self.variable_names)
        variable_to_download_names = variable_names.copy()
        for variable_name in variable_names:
            if not self.task_mng.get('download__{}'.format(variable_name)):
                variable_to_download_names.discard(variable_name)

        # Download variables
        if variable_to_download_names:
            if not self.cfg.get('no_verbose'):
                svar = ', '.join(
                    str(variable_name) for variable_name in
                    variable_to_download_names)
                self.log.info('Downloading {} {}'.format(
                    ', '.join(self.name.split('__')), svar))

            # Download
            downloaded_variable_names = self.download(
                variable_names=variable_to_download_names, **kwargs)

            # Update task manager with all downloaded variables
            # (even the ones that were not requested)
            if downloaded_variable_names is not None:
                for variable_name in downloaded_variable_names:
                    self.task_mng['download__{}'.format(variable_name)] = False


class Composer(object):
    """Compose functions.
    `Compose(f, g, h, **kwargs)(ds) = h(g(f(ds, **kwargs), **kwargs), **kwargs)`.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        #: Functions to compose.
        self._functions = args

        #: Composed function.
        self.composed = functools.reduce(
            lambda f, g: lambda ds=None, **kwargs_add: g(
                ds=f(ds=ds, **kwargs, **kwargs_add), **kwargs, **kwargs_add),
            self._functions, lambda ds=None, **kwargs_add: ds)

    def __call__(self, ds=None, **kwargs_add):
        """Caller."""
        return self.composed(ds=ds, **kwargs_add)
