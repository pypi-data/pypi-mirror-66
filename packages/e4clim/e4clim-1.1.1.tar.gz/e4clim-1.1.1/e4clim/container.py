"""Container and task manager classes definitions."""
import os
import oyaml as yaml
from collections import MutableMapping, Iterable, OrderedDict


class Container(object):
    """Container including a mediator, a configuration,
    and a name."""

    def __init__(self, med, name, cfg=None, task_names=set(),
                 default_tasks_value=True, children=None,
                 parent=None, **kwargs):
        """Initialize mediator, configuration and name.

        :param med: Mediator.
        :param name: Container name.
        :param cfg: Container configuration. Default is `None`.
        :param task_names: Names of potential tasks for container to perform.
          Default is `set()`.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none. Default is `True`.
        :param children: Set of all containers attached to this container.
        :param parent: Parent container.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        :type task_names: set
        :type default_tasks_value: bool
        :type children: :py:class:`set` of :py:class:`Container`
        :type parent: :py:class:`Container`
        """
        #: Mediator.
        self.med = med

        #: Mediator logger.
        self.log = self.med.log

        #: Configuration.
        self.cfg = cfg

        #: Name.
        self.name = name

        #: Containers depending this one.
        self.children = OrderedDict()

        #: Parent container.
        self.parent = None

        # Set parent
        self.set_parent(parent)

        # Update children
        self.update_children(children)

        #: Task manager.
        self.task_mng = TaskManager(
            self, task_names, default_tasks_value=default_tasks_value)

    def set_parent(self, parent, **kwargs):
        if parent is not None:
            # Set parent
            self.parent = parent

            # Add child to parent
            self.parent.update_children({self.name: self})

    def update_children(self, children, **kwargs):
        """Add children to data source and set parent of each child.

        :param children: Children containers to add.
        :type variable_name: mapping of :py:class:`Container`
        """
        if children is not None:
            # Add children
            self.children.update(children)

            # Set parent
            for child in children.values():
                child.parent = self

    def reload_config(self, cfg=None):
        """Reload container configuration and children configurations
        from given/existing mediator configuration.

        :param cfg: Mediator configuration.
        :type cfg: mapping

        .. seealso:: :py:func:`load_config`
        """
        # Reload container configuration
        self.cfg = load_config(self.med, self.name, self.parent)

        # Reload children configurations
        for child in self.children.values():
            child.cfg = load_config(self.med, child.name, self)

    def get_data_dir(self, makedirs=True, **kwargs):
        """Get path to data directory.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Data directory path.
        :rtype: str
        """
        return self.med.cfg.get_project_data_directory(
            self, makedirs=makedirs, **kwargs)


class TaskManager(MutableMapping):
    """Task manager."""

    def __init__(self, container, task_names, default_tasks_value=True,
                 **kwargs):
        """Initialize task manager and ask to perform all tasks, or not.

        :param container: Container.
        :param task_names: Task names.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none. Default is `True`.
        :type container: :py:class:`Container`
        :type task_names: set
        :type default_tasks_value: bool
        """
        # Attach container to its task manager
        self.container = container
        self.name = '{}__task_manager'.format(self.container.name)

        # Initialize tasks
        self.task_names = (ensure_collection(task_names, set)
                           if task_names is not None else set())
        self.task = OrderedDict()
        if self.task_names:
            self.set_all(default_tasks_value)

    def update(self, task_dict):
        """Set given task(s) to given value(s). If a task name
        does not exist yet, it is created and its state set to value.

        :param task_dict: Task (name, value) pairs.
        :type task_dict: :py:class`dict` with :py:class:`bool` values
        """
        for task_name, value in task_dict.items():
            # Add each single task
            self[task_name] = value

    def __setitem__(self, task_name, value):
        """Set single given task.

        :param task_name: Task name to set.
        :param value: Task state value.
        :type task_name: str
        :type value: bool
        """
        # Add task if needed
        if task_name not in self.task_names:
            self.task_names.add(task_name)

        # Set task to value
        self.task[task_name] = value

    def set_all(self, value=True, task_names=None):
        """Set all tasks to given value.

        :param value: State value with which to set all tasks.
          Default is `True` for all tasks.
        :param task_names: Name of task(s) to set. Default is `None`,
          in which case all tasks are set.
        :type value: bool
        :type task_names: (collection of) :py:class:`str`

        .. note:: A task is made more precise by adding `__`
          separated words, e.g. `'load__capacity_factor'`.
          To update all `'load'` tasks, `'load'` can then simply be given.
        """
        # Interesect given and available task names
        valid_task_names = (self.task_names if task_names is None else
                            ensure_collection(task_names, set))
        avail_task_names = set()
        valid_task_names_list = [task.split('__') for task in valid_task_names]
        task_names_list = [task.split('__') for task in self.task_names]
        for task_name in valid_task_names_list:
            for avail_task in task_names_list:
                if avail_task[:len(task_name)] == task_name:
                    avail_task_names.add('__'.join(avail_task))

        # Update container tasks
        self.update({tn: value for tn in avail_task_names})

        # Update children tasks
        for child in self.container.children.values():
            child.task_mng.set_all(value, task_names)

    def __getitem__(self, key):
        """Get item from :py:attr:`task`."""
        return self.task[key]

    def __contains__(self, key):
        """:py:attr:`task` contains."""
        return key in self.task

    def __delitem__(self, key):
        # Remove task from dictionary
        del self.task[key]
        # Remove task name from set
        self.task_names.discard(key)

    def __iter__(self):
        """Iterate :py:attr:`task`."""
        return iter(self.task)

    def __len__(self, key, value):
        """Length of :py:attr:`task`."""
        return len(self.task)

    def __str__(self):
        """Get string of container and its children's tasks."""
        s = '{}: {}'.format(self.container.name, str(self.task))
        for child in self.container.children.values():
            s += '\n  ' + '\n  '.join(str(child.task_mng).split('\n'))

        return s

    def get(self, key, default=None):
        """Get item from :py:attr:`task`."""
        return self.task.get(key, default)


def ensure_collection(arg, collection_type=list):
    """Make a list containing argument or cast iterable to list.

    :param arg: Argument from which to make list.
    :param collection_type: Collection type. Default is `list`.
    :type arg: object
    :type collection_type: type

    :returns: Collection containing from argument(s).
    :rtype: :py:obj:`collection_type`

    .. note:: If `None` is given, `None` is returned.
    """
    if arg is not None:
        if isinstance(arg, str) or (not isinstance(arg, Iterable)):
            arg = collection_type([arg])
        else:
            arg = collection_type(arg)

    return arg


def load_config(med, name, parent=None):
    """Load container configuration from main configuration dictionary,
    from given parent, or from file.

    :param med: Mediator.
    :param name: Container name.
    :param parent: Parent container from the configuration of which,
      the configuration of this child container could be gotten.
      Default is `None`.
    :type med: :py:class:`.mediator.Mediator`
    :type name: str
    :type parent: :py:class:`Container`

    :returns: Container configuration.
    :rtype: dict
    """
    cfg_from_parent = parent.cfg.get(name) if parent is not None else None
    user_cfg_path = med.cfg['cfg_path'].get(name)
    if name in med.cfg:
        # Get source configuration from main configuration
        cont_cfg = med.cfg[name]
    elif user_cfg_path:
        # Read source configuration from path
        user_cfg_path = os.path.join(*ensure_collection(user_cfg_path))
        with open(user_cfg_path, 'r') as f:
            cont_cfg = yaml.load(f, Loader=yaml.FullLoader)
    elif parent is not None:
        # Get source configuration from component configuration
        cont_cfg = cfg_from_parent
    else:
        # None worked, no configuration found
        cont_cfg = None
        med.log.warning('No {} configuration found'.format(name))

    return cont_cfg
