"""Mediator configuration management."""
import os
from collections import MutableMapping
from importlib import import_module
import oyaml as yaml
from getpass import getpass
from .container import ensure_collection


def input_expand_user(fun):
    """Decorator of :py:func:`input` to manage `'~'` in filepath."""
    def decorated_fun(prompt):
        q = fun(prompt)
        return os.path.expanduser(q)

    return decorated_fun


# Decorate open to manage ~ in paths with decorator_expand_user
input = input_expand_user(input)


class Config(MutableMapping):
    """Configuration class."""

    def __init__(self, pre_config_filepath=None):
        """Load configuration file.

        :param pre_config_filepath: Filepath of (pre-)configuration file.
          If `None`, ask user. Default is `None`.
        :type pre_config_filepath: str
        """
        #: Actual configuration.
        self.cfg = None

        if not pre_config_filepath:
            # Ask for the configuation file
            default_cfg_filepath = os.path.join('cfg', 'which_config.yaml')
            pre_config_filepath = input(
                'Mediator configuration filepath ([{}]): '.format(
                    default_cfg_filepath))
            if not pre_config_filepath:
                pre_config_filepath = default_cfg_filepath

        # Open pre-configuration file
        with open(pre_config_filepath, 'r') as f:
            precfg = yaml.load(f, Loader=yaml.FullLoader)

        if 'cfg_filepath' in precfg:
            # If pre-configuration file has a configuration filename,
            # load the target configuration file
            cfg_filepath = precfg['cfg_filepath']
            print('Loading configuration from '.format(cfg_filepath))
            with open(cfg_filepath, 'r') as f:
                self.cfg = yaml.load(f, Loader=yaml.FullLoader)
        else:
            # Else, return the pre-configuration
            self.cfg = precfg

    def get_credentials(self, name, keys=['user', 'passwd']):
        """Get credentials given by :py:obj:`keys` argument
        for a container named :py:obj:`name` from file, or ask them.

        :param name: Container name.
        :param keys: Name of asked credentials.
        :type name: str
        :type keys: list

        :returns: Credential key-value pairs.
        :rtype: dict
        """
        # Get credentials
        keys_path = os.path.join(*ensure_collection(
            self.cfg['cfg_path']['keys']))
        if os.path.isfile(keys_path):
            # Try to get them from keys file
            with open(keys_path, 'r') as f:
                cfg_keys = yaml.load(f, Loader=yaml.FullLoader)

            # Get or create container credentials dictionary
            if not isinstance(cfg_keys.get(name), MutableMapping):
                cfg_keys[name] = {}
            cred = cfg_keys[name]
        else:
            cfg_keys = {name: {}}
            cred = {}

        any_new = False
        for k in keys:
            if cred.get(k) is None:
                # Get credential value for key
                cred[k] = getpass('{} {}: '.format(name, k))
                any_new = True

        if any_new:
            # Ask if user wants to save keys to keys file
            q = None
            while q not in ['no', 'yes', '']:
                q = input(
                    'Save new redentials to {} ([yes]/no)? '.format(
                        keys_path))
            if q in ['yes', '']:
                with open(keys_path, 'r+') as f:
                    yaml.dump(cfg_keys, f, default_flow_style=False)

        # Return only asked key-value pairs
        return {k: cred.get(k) for k in keys}

    def get_data_root_directory(self, **kwargs):
        """Get data root directory from mediator configuration.

        :returns: Data root-directory.
        :rtype: str
        """
        directory = self.get('data_dir')
        directory = ('data' if directory is None else
                     os.path.join(*ensure_collection(directory)))

        return directory

    def get_project_data_directory(
            self, container=None, makedirs=True, subdirs=None, **kwargs):
        """Get project data directory and create it if needed.

        :param container: Container for which to get data directory.
        :param makedirs: Make directories if needed. Default is `True`.
        :param subdirs: List of additional subdirectories.
        :type container: :py:class:`.container.Container`
        :type makedirs:
        :type subdirs: :py:class:`str` or :py:class:`list` or :py:class:`str`

        :returns: Directory path.
        :rtype: str
        """
        subdirs = ensure_collection(subdirs)
        base_subdir = self['project_name']
        base_dir = os.path.join(self.get_data_root_directory(**kwargs),
                                base_subdir)
        if container:
            user_project_dir = container.med.cfg.get('project_dir')
            directory = (os.path.join(base_dir, container.name)
                         if user_project_dir is None else
                         os.path.join(*ensure_collection(user_project_dir)))
        else:
            directory = base_dir
        if subdirs is not None:
            directory = os.path.join(directory, *subdirs)

        if makedirs:
            # Create directory if needed
            os.makedirs(directory, exist_ok=True)

        return directory

    def get_external_data_directory(
            self, container=None, makedirs=True, subdirs=None, **kwargs):
        """Get external data directory and create it if needed.

        :param container: Data source for which to get data directory.
        :param makedirs: Make directories if needed. Default is `True`.
        :param subdirs: List of additional subdirectories.
        :type container: :py:class:`.data_source.DataSourceBase`
        :type makedirs: bool
        :type subdirs: :py:class:`str` or :py:class:`list` or :py:class:`str`

        :returns: Directory path.
        :rtype: str
        """
        subdirs = ensure_collection(subdirs)
        base_subdir = 'extern'
        base_dir = os.path.join(self.get_data_root_directory(**kwargs),
                                base_subdir)
        if container:
            user_data_dir = container.cfg.get('data_dir')
            directory = (os.path.join(base_dir, container.name)
                         if user_data_dir is None else
                         os.path.join(*ensure_collection(user_data_dir)))
        else:
            directory = base_dir
        if subdirs is not None:
            directory = os.path.join(directory, *subdirs)

        if makedirs:
            # Create directory if needed
            os.makedirs(directory, exist_ok=True)

        return directory

    def get_plot_root_directory(self, **kwargs):
        """Get plot root directory from mediator configuration.

        :returns: Plot root-directory.
        :rtype: str
        """
        directory = self.get('plot_dir')
        directory = ('plot' if directory is None else
                     os.path.join(*ensure_collection(directory)))

        return directory

    def get_plot_directory(
            self, container=None, makedirs=True, subdirs=None, **kwargs):
        """Get project data directory and create it if needed.

        :param container: Container for which to get data directory.
        :param makedirs: Make directories if needed. Default is `True`.
        :param subdirs: List of additional subdirectories.
        :type container: :py:class:`.container.Container`
        :type makedirs:
        :type subdirs: :py:class:`str` or :py:class:`list` or :py:class:`str`

        :returns: Directory path.
        :rtype: str
        """
        subdirs = ensure_collection(subdirs)
        base_dir = os.path.join(self.get_plot_root_directory(**kwargs),
                                self['project_name'])

        directory = (os.path.join(base_dir, container.name)
                     if container is not None else base_dir)
        if subdirs is not None:
            directory = os.path.join(directory, *subdirs)

        if makedirs:
            # Create directory if needed
            os.makedirs(directory, exist_ok=True)

        return directory

    # Interface with cfg dictionary
    def __getitem__(self, key):
        """Get item from :py:attr:`cfg`."""
        return self.cfg[key]

    def __setitem__(self, key, value):
        """Set item in :py:attr:`cfg`."""
        self.cfg[key] = value

    def __contains__(self, key):
        """:py:attr:`cfg` contains."""
        return key in self.cfg

    def __delitem__(self, key):
        del self.cfg[key]

    def __iter__(self):
        """Iterate :py:attr:`cfg`."""
        return iter(self.cfg)

    def __len__(self, key, value):
        """Length of :py:obj:`cfg`."""
        return len(self.cfg)

    def __str__(self):
        """Return `str(self.cfg)`."""
        return str(self.cfg)

    def get(self, key, default=None):
        """Get item from :py:attr:`cfg`."""
        return self.cfg.get(key, default)


def import_module_from_cfg(cfg, name='', module_path=None):
    """Import actuator module from some container configuration.

    :param cfg: Configuration used to import module of container.
    :param name: Container name. Default is `''`.
    :param module_path: Module path. Default is `None`, in which
      case the module path is read from the `module_path` entry
      of the configuration.
    :type cfg: mapping
    :type name: str
    :type module_path: str

    :returns: Actuator module.
    :rtype: module
    """
    module_path = module_path or cfg.get('module_path')
    return (import_module(module_path, package=__package__)
            if module_path is not None else None)
