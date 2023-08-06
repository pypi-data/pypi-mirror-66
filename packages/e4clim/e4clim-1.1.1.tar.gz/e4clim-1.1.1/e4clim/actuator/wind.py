"""Wind-farm model definition."""
from pkg_resources import resource_stream
import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
import xarray as xr
from ..utils.climate import (get_air_density_at_height, get_wind_at_height,
                             get_wind_magnitude)
from ..data_source import Composer
from ..actuator_base import ExtractorBase

#: Available-dataset names.
VARIABLE_NAMES = ['generation', 'capacity_factor']


class Actuator(ExtractorBase):
    """Wind-farm model."""
    #: Default result name.
    DEFAULT_RESULT_NAME = 'capacity_factor'

    def __init__(self, result_mng, name, cfg=None, **kwargs):
        """Naming constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Actuator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping
        """
        if result_mng.name != self.DEFAULT_RESULT_NAME:
            self.log.warning(
                'Result name {} given to constructor does not correspond '
                'to {} to be estimated by {}'.format(
                    result_mng.result_name, self.DEFAULT_RESULT_NAME,
                    self.name))

        super(Actuator, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg,
            variable_names=VARIABLE_NAMES, **kwargs)

        #: Required input-variables.
        self.input_variable_names = set()

        #: Power-curve speeds.
        self.speed_curve = None
        #: Power-curve powers.
        self.power_curve = None
        #: Power-curve function.
        self.power_fun = None
        #: Cut-in speed.
        self.cut_in_speed = None
        #: Cut-out speed.
        self.cut_out_speed = None
        #: Rated power.
        self.rated_power = None
        #: Rated-power speed.
        self.rated_power_speed = None

        # Read power curve, interplate and get thresholds
        self.get_power_curve()

    def update_input_variable_names(self, data_src):
        """Add input variables available in data source.

        :param data_src: Input data source.
        :type data_src: :py:class:`..grid.GriddedDataSourceBase`
        """
        if self.cfg.get('use_roughness'):
            self.input_variable_names.add('roughness_height')
        if 'wind_magnitude' in data_src:
            self.input_variable_names.add('wind_magnitude')
        else:
            self.input_variable_names.update(['zonal_wind', 'meridional_wind'])
        if 'surface_density' in data_src:
            self.input_variable_names.add('surface_density')
        if 'surface_specific_humidity' in data_src:
            self.input_variable_names.add('surface_specific_humidity')
        if 'surface_pressure' in data_src:
            self.input_variable_names.add('surface_pressure')
        if 'surface_temperature' in data_src:
            self.input_variable_names.add('surface_temperature')
        if ((not ('surface_pressure' in data_src)) and
                ('sea_level_pressure' in data_src)):
            self.input_variable_names.add('sea_level_pressure')

    def transform(self, data_src, stage=None, **kwargs):
        """Compute wind electricity generation from climate data.

        :param data_src: Input data source.
        :param stage: Modeling stage: `'fit'` or `'predict'`.
          May be required if features differ in prediction stage.
        :type data_src: :py:class:`..grid.GriddedDataSourceBase`
        :type stage: str

        :returns: Transformed dataset.
        :rtype: :py:class:`xarray.Dataset`
        """
        # Update available input variables set
        self.update_input_variable_names(data_src)

        # Functions to apply to the input climate data
        functions = ([data_src.add_roughness_height]
                     if self.cfg.get('use_roughness') else [])

        # Add regions domain cropping
        functions.extend([data_src.crop_area, get_wind_magnitude])

        if hasattr(self.result_mng, 'modifier'):
            if (hasattr(self.result_mng.modifier.cfg, 'stage') and
                    (self.result_mng.modifier.cfg['stage'] != stage)):
                pass
            else:
                # Add modifier transformation
                functions.append(self.result_mng.modifier.transform)

        # Add get generation and get regional mean
        functions.extend([self.get_generation, data_src.get_regional_mean])

        # Get wind generation from climate data
        ds = data_src.load(transform=Composer(*functions),
                           variable_names=self.input_variable_names)

        return ds

    def get_generation(self, ds, data_src, **kwargs):
        """Compute wind electricity generation from daily climate dataset.

        :param ds: Dataset containing all climate variables of interest.
        :param data_src: Data source object from which to get feature.
        :type ds: :py:class:`xarray.Dataset`
        :type data_src: :py:class:`..grid.GriddedDataSourceBase`

        :returns: A dataset containing electricity generation.
        :rtype: :py:class:`xarray.DataArray`

        .. note::
          * The dataset should contain a `lat` and a `lon` coordinate
            variables.
          * The dataset should contain `zonal_wind` and `meridional_wind`
            variables for the zonal
            and meridional surface wind velocity.
          * If the `surface_temperature`, `surface_pressure`
            and `surface_specific_humidity` variables are given,
            the surface density
            is computed from the surface atmospheric temperature, pressure
            and specific humidity, respectively.
        """
        roughness_height = (ds['roughness_height']
                            if self.cfg.get('use_roughness') else None)

        if 'wind_magnitude' in ds:
            speed = ds['wind_magnitude']
        else:
            # Get magnitude of wind speed from wind components
            speed = get_wind_magnitude(ds, **kwargs)

        if not self.cfg.get('no_verbose'):
            self.log.info('Getting wind speed at 100m from 10m wind')
        z_0_wind = float(ds['zonal_wind'].attrs['height'])
        hub_speed = get_wind_at_height(
            speed, z=self.cfg['hub_height'],
            z_0=z_0_wind, roughness_height=roughness_height)

        # Get air density if possible
        if 'surface_density' in ds:
            # Check if surface density is given
            rho = ds['surface_density']
        else:
            # Compute density, if at least surface temperature
            # and pressure are given
            if not self.cfg.get('no_verbose'):
                self.log.info('Computing density')
            rho = get_air_density_at_height(ds, self.cfg['hub_height'])

        # Get wind power
        mean_speed2mean_gen = False
        # data_freq = ds.indexes['time'].inferred_freq.upper()
        # if data_freq in ['D', '1D']:
        #     if self.med.cfg['frequency'] == 'day':
        #         # Take the variance of speed into account assuming Rayleigh
        #         mean_speed2mean_gen = True
        #     elif self.med.cfg['frequency'] == 'hour':
        #         self.log.info('Up-sampling wind speed')
        #         # Upsample from daily to hourly values
        #         end_time = rho.indexes['time'][-1] + pd.Timedelta(23, unit='H')
        #         t = pd.date_range(
        #             start=rho.indexes['time'][0], end=end_time, freq='H')
        #         hub_speed = upsample_wind_speed(hub_speed)
        #         # hub_speed = hub_speed.reindex(time=t).ffill('time')
        #         rho = rho.reindex(time=t).ffill('time')

        if not self.cfg.get('no_verbose'):
            self.log.info('Getting wind power')
        self.generation = self.get_wind_generation(
            hub_speed, rho=rho, mean_speed2mean_gen=mean_speed2mean_gen)

        if self.med.cfg['frequency'] == 'day':
            if data_src.cfg['frequency'] == 'hour':
                # Downsample generation
                self.generation = self.generation.resample(
                    time='D').sum('time')
            else:
                # Convert from daily mean to daily integral
                self.generation *= 24
            generation_units = 'Wh/d'
        elif self.med.cfg['frequency'] == 'hour':
            generation_units = 'Wh'

        # Get capacity factors
        self.capacity_factor = self.generation / self.rated_power
        if self.med.cfg['frequency'] == 'day':
            self.capacity_factor /= 24

        # Try to add attributes (should be xarray.DataArray)
        try:
            self.capacity_factor.name = self.result_mng.result_name
            self.capacity_factor.attrs['long_name'] = 'Wind Capacity Factor'
            self.capacity_factor.attrs['units'] = ''
            self.generation.attrs['units'] = generation_units
        except AttributeError:
            pass

        ds = xr.Dataset({variable_name: getattr(self, variable_name)
                         for variable_name in VARIABLE_NAMES})

        return ds

    def get_extractor_postfix(self, **kwargs):
        """Get postfix corresponding to wind features.

        returns: Postfix.
        rtype: str
        """
        postfix = '{}_{}'.format(
            super(Actuator, self).get_extractor_postfix(**kwargs),
            self.med.cfg['frequency'])

        if self.cfg.get('use_roughness'):
            postfix += '_logheight'

        return postfix

    def get_power_curve(self):
        """Read and interpolate power curve.

        .. note::
          * Power curve should be an array with the wind speed and
            corresponding power as first and second columns, respectively.
          * For the interpolation, splines with cut-in, cut-out and rated
            output speeds are used to avoid large jumps in power distribution.
        """
        resource_name = '../data/{}'.format(self.cfg['powercurve_filename'])
        with resource_stream(__name__, resource_name) as f:
            power_data = pd.read_csv(f, index_col=0)

        # Power curve interpolation:
        self.speed_curve = power_data.index
        self.power_curve = power_data.values[:, 0]
        self.power_fun = interp1d(
            self.speed_curve, self.power_curve,
            kind='cubic', fill_value=0., bounds_error=False)

        # Cut-in speed
        id_cut_in = np.nonzero(self.power_curve > 0.1)[0][0]
        self.cut_in_speed = self.speed_curve[id_cut_in]

        # Cut-out speed
        id_cut_out = (np.nonzero(self.power_curve[id_cut_in:] > 0.1)[0][-1]
                      + id_cut_in)
        self.cut_out_speed = self.speed_curve[id_cut_out]

        # Rated power
        self.rated_power = np.max(self.power_curve)
        id_rated_power = np.nonzero(np.abs(
            self.rated_power - self.power_curve) < 0.1)[0][0]
        self.rated_power_speed = self.speed_curve[id_rated_power]

    def get_wind_generation(self, speed, rho=None, rho0=1.225,
                            mean_speed2mean_gen=False):
        """Compute wind power from a manufacturer's power curve.

        :param speed: Wind speed (m/s).
        :param rho: Air density (kg/m3). If None, air density
          is taken as the reference density for which the power curve
          was obtained. Default is None.
        :param rho0: Reference air density (kg/m3) for which the
          power curve was obtained. Default is 1.225 (kg/m3).
        :param mean_speed2mean_gen: If True, :py:obj:`speed`
          is taken as the mean of a Rayleigh distribution
          so that a factor :math:`(6 / \pi)^{1/3}` is applied to the
          mean wind speed to get the corresponding mean wind power.
          Default is False.
        :type speed: (sequence of) :py:class:`float`
        :type rho: (sequence of) :py:class:`float`
        :type rho0: float
        :type mean_speed2mean_gen: bool

        :returns: Wind power (W).
        :rtype: :py:class:`xarray.DataArray`
        """
        speed_eq = speed.copy(deep=True)

        # Conversion of wind speed for a different density
        if rho is not None:
            speed_eq *= (rho / rho0)**(1. / 3)

        # Factor accounting for the fact that mean wind power
        # is computed from mean wind speed
        if mean_speed2mean_gen:
            speed_eq *= (6. / np.pi)**(1. / 3)

        # Threshold. Use where function instead of method to keep as
        # original numpy.array
        try:
            generation = xr.full_like(speed_eq, None)
            generation[:] = self.power_fun(speed_eq)
        except TypeError:
            generation = self.power_fun(speed_eq)
        generation = xr.where((speed_eq > self.cut_in_speed) &
                              (speed_eq < self.cut_out_speed),
                              generation, 0.)
        generation = xr.where(speed_eq < self.rated_power_speed,
                              generation, self.rated_power)
        generation = xr.where(generation <= self.rated_power,
                              generation, self.rated_power)

        try:
            generation.name = 'generation'
            generation.attrs['long_name'] = 'Wind Generation'
            generation.attrs['units'] = 'Wh'
        except AttributeError:
            pass

        return generation


def upsample_wind_speed(speed):
    """Up-sample wind speed from daily to hourly values
    assuming that intra-day values follow a Rayleigh distribution
    with mean that of the given wind-speed time-series.

    :param speed: Daily wind-speed time-series.
    :type speed: :py:class:`xarray.DataArray`

    :returns: Hourly wind-speed.
    :rtype: :py:class:`xarray.DataArray`
    """
    # Upsample from daily to hourly values uniformly
    n_hours = 24
    delta_day = pd.Timedelta(n_hours - 1, unit='H')
    end_time = speed.indexes['time'][-1] + delta_day
    t = pd.date_range(start=speed.indexes['time'][0], end=end_time, freq='H')
    speed_up = speed.reindex(time=t)

    # Loop over days
    fact = np.sqrt(2 / np.pi)
    coords_space = [speed.coords[dim] for dim in speed.dims if dim != 'time']
    shape_space = [len(coord) for coord in coords_space]
    nspeedal = np.empty([n_hours] + shape_space)
    for date in speed.indexes['time']:
        # Get std predicted by Rayleigh distribution
        sigma = speed.loc[{'time': date}] * fact

        # Create noise array
        time_day = pd.date_range(
            start=date, end=(date + delta_day), freq='H')
        nspeedal[:] = [np.random.rayleigh(sigma) for h in range(n_hours)]
        coords = [('time', time_day)] + coords_space
        day_noise = xr.DataArray(nspeedal, coords=coords)

        # Add white noise to increase variance
        speed_up.loc[{'time': slice(time_day[0], time_day[-1])}] = day_noise

    return speed_up
