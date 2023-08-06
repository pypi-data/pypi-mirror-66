"""Photovoltaic farm model definition."""
import pandas as pd
import xarray as xr
from ..utils.climate import get_temperature_at_height
from ..utils.radiation import HorizontalRadiationComputer
from ..utils.radiation import TiltedRadiationComputer
from ..data_source import Composer
from ..actuator_base import ExtractorBase

#: Available-dataset names.
VARIABLE_NAMES = [
    'global_horizontal_et', 'global_horizontal_surf',
    'global_tilted_surf', 'generation', 'capacity_factor',
    'cell_efficiency'
]


class Actuator(ExtractorBase):
    """Photovoltaic model."""
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
        self.input_variable_names = {'surface_downward_radiation',
                                'surface_temperature'}

        #: Global horizontal surface irradiance.
        self.global_horizontal_surf = None
        #: Global horizontal extraterrestrial irradiance.
        self.global_horizontal_et = None
        #: Global tilted surface irradiance.
        self.global_tilted_surf = None
        #: Clearness index.
        self.clearness_index = None
        #: Generation.
        self.generation = None
        #: Cell efficiency.
        self.cell_efficiency = None
        #: Capacity factor.
        self.capacity_factor = None

    def transform(self, data_src, stage=None, **kwargs):
        """Compute photovoltaic electricity generation from climate data.

        :param data_src: Input data source.
        :param stage: Modeling stage: `'fit'` or `'predict'`.
          May be required if features differ in prediction stage.
        :type data_src: :py:class:`..grid.GriddedDataSourceBase`
        :type stage: str

        :returns: Transformed dataset.
        :rtype: :py:class:`xarray.Dataset`
        """
        # Add regions domain cropping
        functions = [data_src.crop_area]

        if hasattr(self.result_mng, 'modifier'):
            if (hasattr(self.result_mng.modifier.cfg, 'stage') and
                    (self.result_mng.modifier.cfg['stage'] != stage)):
                pass
            else:
                # Add modifier transformation
                functions.append(self.result_mng.modifier.transform)

        # Add get generation and get regional mean
        functions.extend([self.get_generation, data_src.get_regional_mean])

        # Get pv generation from climate data
        ds = data_src.load(transform=Composer(*functions),
                           variable_names=self.input_variable_names)

        return ds

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        postfix = '{}_{}'.format(
            super(Actuator, self).get_extractor_postfix(**kwargs),
            self.med.cfg['frequency'])

        return postfix

    def get_generation(self, ds, data_src, **kwargs):
        """Compute the photovoltaic electricity generation
        from the daily climate dataset.

        :param ds: Dataset containing climate variables from which to
          compute generation.
        :param data_src: Data source object from which to get features.
        :type ds: :py:class:`xarray.Dataset`
        :type data_src: :py:class:`..grid.GriddedDataSourceBase`

        :returns: A dataset containing the electricity generation.
        :rtype: :py:class:`xarray.Dataset`

        .. note::
          * The dataset should contain a `lat` and a `lon` coordinate
            variables.
          * The dataset should contain a `surface_downward_radiation` variable
            for the global horizontal radiation at the surface.
          * If the dataset contains a `surface_temperature` variable
            for the surface temperature,
            the temperature dependent cell efficiency is computed.
          * If the dataset contains a `surface_temperature` variable
            for the surface temperature,
            the temperature dependent cell efficiency is computed.

        .. warning:: Time index in dataset :py:obj:`ds` should be UTC.
        """
        # Get HOURLY time index (UTC)
        time = ds.indexes['time']
        freq_data = time.inferred_freq.upper()
        if freq_data in ['D', '1D']:
            time = pd.date_range(start=time[0], freq='H',
                                 end=(time[-1] + pd.Timedelta(23, 'H')))

        # Get surface temperature
        temp_a = None
        if 'surface_temperature' in ds:
            temp_0 = ds['surface_temperature']
            z_0 = float(temp_0.attrs[data_src.cfg['height']])

            # Adjust to surface temperature (2m)
            temp_a = get_temperature_at_height(temp_0, z_0, 2.)

        # Get hourly global horizontal extraterrestrial radiation
        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Getting hourly global extraterrestrial solar radiation')
        rc_hour = HorizontalRadiationComputer(
            time, ds.lat, ds.lon,
            global_horizontal_surf=ds['surface_downward_radiation'],
            angles_in_degrees=True)
        self.global_horizontal_et = rc_hour.global_horizontal_et

        # Recycle solar computer
        sc_hour = rc_hour.sc

        if freq_data in ['D', '1D']:
            # Up-sample temperature
            temp_a = temp_a.resample(time='H').ffill().reindex(
                time=time, method='ffill')

            # Get daily-mean global horizontal extraterrestrial radiation
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Getting daily-mean global horizontal extraterrestrial '
                    'solar radiation')
            global_horizontal_et_day = self.global_horizontal_et.resample(
                time='D').mean('time', keep_attrs=True)
            global_horizontal_surf_day = ds['surface_downward_radiation']

            # Get clearness index from DAILY-averaged
            # toa and surface radiations
            if not self.cfg.get('no_verbose'):
                self.log.info('Getting daily-mean clearness index')
            rc_day = HorizontalRadiationComputer(
                time, ds.lat, ds.lon,
                global_horizontal_et=global_horizontal_et_day,
                global_horizontal_surf=global_horizontal_surf_day,
                angles_in_degrees=True)
            clearness_index_day = rc_day.clearness_index

            # Up-sample daily clearness index to hourly
            if not self.cfg.get('no_verbose'):
                self.log.info('Up-sampling clearness index to hours')
            self.clearness_index = clearness_index_day.resample(
                time='H').ffill().reindex(time=time, method='ffill')

            # Radiations computation from clearness index and hourly
            # global horizontal extraterrestrial radiation
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Getting hourly global horizontal surface radiation from '
                    'hourly horizontal extraterrestrial radiation and '
                    'up-sampled clearness index')
            rc_hour = TiltedRadiationComputer(
                time, ds.lat, ds.lon,
                global_horizontal_et=self.global_horizontal_et,
                clearness_index=self.clearness_index,
                angles_in_degrees=True, **self.cfg['surface'],
                solar_computer=sc_hour)

            self.global_horizontal_surf = rc_hour.global_horizontal_surf

        elif freq_data in ['H', '1H']:
            # Radiations computation from hourly global horizontal
            # extraterrestrial and surface radiation (from source)
            self.global_horizontal_surf = ds['surface_downward_radiation']
            rc_hour = TiltedRadiationComputer(
                time, ds.lat, ds.lon,
                global_horizontal_et=self.global_horizontal_et,
                global_horizontal_surf=self.global_horizontal_surf,
                angles_in_degrees=True, **self.cfg['surface'],
                solar_computer=sc_hour)

        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Computing hourly global tilted surface radiation')
        self.global_tilted_surf = rc_hour.global_tilted_surf

        # Get hourly solar generation
        if not self.cfg.get('no_verbose'):
            self.log.info('Computing hourly photovoltaic generation')
        self.generation, self.cell_efficiency = get_pv_power(
            self.global_tilted_surf, temp_a, **self.cfg['module'],
            return_efficiency=True)

        # Get hourly capacity factor
        self.capacity_factor = (
            self.generation / self.cfg['module']['nominal_power'])

        # Save key variables in object (e.g. for plots)
        if self.med.cfg['frequency'] == 'day':
            # Add daily-integrated variables to dataset
            if not self.cfg.get('no_verbose'):
                self.log.info('Resampling from hourly to daily frequency')
            for variable_name in VARIABLE_NAMES:
                setattr(self, variable_name, getattr(
                    self, variable_name).resample(time='D').sum(
                        'time', keep_attrs=True))

            # Manage daily units
            generation_units = 'Wh/d'
            self.capacity_factor /= 24
        else:
            generation_units = 'Wh'

        try:
            self.capacity_factor.name = self.result_mng.result_name
            self.capacity_factor.attrs['long_name'] = (
                'Photovoltaic Capacity Factor')
            self.capacity_factor.attrs['units'] = ''
            self.generation.attrs['units'] = generation_units
        except AttributeError:
            pass

        ds = xr.Dataset({variable_name: getattr(self, variable_name)
                         for variable_name in VARIABLE_NAMES})

        return ds


def get_pv_power(global_tilted_surf, temp_a=None, wind_speed=1., area=1.675,
                 n_modules=1, eff_elec=0.86, eff_cell=None, thermal_loss=0.004,
                 temp_ref=298.15, temp_cell_noct=319.15, nominal_power=None,
                 return_efficiency=False):
    """Set photovoltaic power from inclinaison, clearness index
    and surface air temperature.

    :param global_tilted_surf: Global tilted surface radiation
      (W/m2, or Wh/m2/h).
    :param temp_a: Surface air temperature (K).
      If None, the temperature of the cell is considered to be the same
      as the reference temperature temp_ref.
      Default is None.
    :param wind_speed: Magnitude of the wind velocity (m/s).
    :param area: Area of each module (m2). Default is 1.675 (m2).
    :param n_modules: Number of modules. Default is 1.
    :param eff_elec: Efficiency of the electronics
      (inverter, array and power conditionning, etc.). Default is 0.86.
    :param eff_cell: Efficiency of the cell at the reference temperature
      temp_ref. If None, compute it from the nominal power. Default is None.
    :param thermal_loss: Efficiency loss per degree Kelvin
      away from the reference temperature. Default is
      :math:`0.0041~\mathrm{K}^{-1}`.
    :param temp_ref: Reference temperature (K). Default 298.15 K.
    :param temp_cell_noct: Cell temperature at the
      Nominal Operating Cell Temperature (NOCT) (K).
      Default is 319.15 K.
    :param nominal_power: Nominal power of the module (W). See note.
      Only used to compute the efficiency of the cell eff_cell
      at the reference temperature temp_ref if eff_cell is not given.
    :param return_efficiency: If True, return the temperature dependent
      cell efficiency. Default is False.
    :type global_tilted_surf: (sequence of) :py:class:`float`
    :type temp_a: (sequence of) :py:class:`float`
    :type wind_speed: (sequence of) :py:class:`float`
    :type area: float
    :type n_modules: int
    :type eff_elec: float
    :type eff_cell: float
    :type thermal_loss: float
    :type temp_ref: float
    :type temp_cell_noct: float
    :type nominal_power: float
    :type return_efficiency: bool

    :returns: Electric power delivered by the array (W/m2, or Wh/m2/h).
    :rtype: (:py:class:`tuple` of) (sequence of) :py:class:`float`

    .. warning::
      The global tilted radiation `global_tilted_surf` should be given as
      power in W/m2, or as averaged power in Wh/m2/h to avoid erros
      in cell efficiency computations.
    """
    # Temperature dependent efficiency of the cell
    eff_cell_t = get_cell_efficiency(
        temp_a=temp_a, global_tilted_surf=global_tilted_surf, area=area,
        wind_speed=wind_speed, eff_cell=eff_cell, thermal_loss=thermal_loss,
        temp_ref=temp_ref, temp_cell_noct=temp_cell_noct,
        nominal_power=nominal_power)

    # Electric power delivered by the array
    generation = area * n_modules * eff_elec * eff_cell_t * global_tilted_surf

    # Name power if possible
    try:
        generation.name = 'generation'
        generation.attrs['long_name'] = 'Photovoltaic Array Generation'
        generation.attrs['units'] = (
            '{:s}'.format(global_tilted_surf.units.strip('/ m2'))
            if hasattr(global_tilted_surf, 'units') else 'Wh')
    except AttributeError:
        pass

    return (generation, eff_cell_t) if return_efficiency else generation


def get_cell_efficiency(
        temp_a=None, global_tilted_surf=800., wind_speed=1., area=1.,
        eff_cell=None, thermal_loss=0.004, temp_ref=298.15,
        temp_cell_noct=319.15, nominal_power=None):
    """Get temperature dependent cell efficiency.

    :param temp_a: Surface air temperature (K).
      If None, the temperature of the cell is considered to be the same
      as the reference temperature temp_ref.
      Default is None.
    :param global_tilted_surf: Global tilted radiation (W/m2, or Wh/m2/h).
      Default is the :py:obj:`global_tilted_surf` at
      Nominal Operating Cell Temperature (_noct).
    :param wind_speed: Magnitude of the wind velocity (m/s).
    :param area: Area of each module (m2). Default is 1 (m2).
      (inverter, array and power conditionning, etc.). Default is 0.86.
    :param eff_cell: Efficiency of the cell at the reference temperature
      temp_ref. If None, compute it from the nominal power. Default is None.
    :param thermal_loss: Efficiency loss per degree Kelvin
      away from the reference temperature. Default is
      :math:`0.0041~\mathrm{K}^{-1}`.
    :param temp_ref: Reference temperature (K). Default 298.15 K.
    :param temp_cell_noct: Cell temperature at _noct (K). Default is 319.15 K.
    :param nominal_power: Nominal power of the module (W). See note.
      Only used to compute the efficiency of the cell eff_cell
      at the reference temperature temp_ref if eff_cell is not given.
    :type temp_a: (sequence of) :py:class:`float`
    :type global_tilted_surf: (sequence of) :py:class:`float`
    :type wind_speed: (sequence of) :py:class:`float`
    :type area: float
    :type eff_cell: float
    :type thermal_loss: float
    :type temp_ref: float
    :type temp_cell_noct: float
    :type nominal_power: float

    :returns: Temperature dependent cell efficiency.
    :rtype: (sequence of) float)

    .. note::
        * The thermal model of Duffie and Beckman (2013)
          is used here to compute the efficiency of the cell
          for a given ambient temperature.
        * The global tilted radiation :py:obj:`global_tilted_surf` should be
          given as power in W/m2, or as averaged power in Wh/m2/h to avoid
          erros in cell efficiency computations.

    .. seealso::
        Duffie, J.A., Beckman, W.A., 2013.
        *Solar Energy and Thermal Processes*, fourth ed. Wiley, Hoboken, NJ.
    """
    # Radiation on module plane at _noct (W/m2)
    global_tilted_surf_noct = 800.
    # Ambient Temperature at _noct (K)
    temp_a_noct = 293.15
    # Light intensity at STC (W/m2). See note.
    ir_std = 1000.

    # If not given, compute cell efficiency from nominal power
    if eff_cell is None:
        eff_cell = (nominal_power / ir_std) / area

    if temp_a is None:
        # If the ambient temperature is not given, the cell temperature
        # is taken as the same as the reference temperature. As a result,
        # the cell efficiency does not depend on the temperature.
        temp_cell = temp_ref
    else:
        # Compute temperature dependent efficiency of module
        # Thermal loss ration: :math:`U_{L, _noct} / U_L`
        loss_ratio = 9.5 / (5.7 + 3.8 * wind_speed)

        # Cell temperature (K). See note.
        # :math:`  au \alpha / U_L = (T_{c, _noct} - T_{a, _noct}) / G_{T, NOCT}`
        temp_cell = (temp_a + (global_tilted_surf / global_tilted_surf_noct)
                     * loss_ratio * (temp_cell_noct - temp_a_noct))

    # Temperature dependent efficiency of the cell
    eff_cell_t = eff_cell * (1 - thermal_loss * (temp_cell - temp_ref))

    # Name
    try:
        eff_cell_t.name = 'cell_efficiency'
        eff_cell_t.attrs['long_name'] = 'Wheather Dependent Cell Efficiency'
        eff_cell_t.attrs['units'] = ''
    except AttributeError:
        pass

    return eff_cell_t
