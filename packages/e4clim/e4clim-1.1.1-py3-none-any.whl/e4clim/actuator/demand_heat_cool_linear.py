"""Linear demand.actuator with heating and cooling days."""
import numpy as np
import pandas as pd
import xarray as xr
from sklearn import linear_model
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.exceptions import NotFittedError
from ..data_source import Composer
from ..actuator_base import ExtractorBase, EstimatorBase
from ..utils.learn import MultiInputRegressor, select_data


class Actuator(ExtractorBase, EstimatorBase):
    #: Default result name.
    DEFAULT_RESULT_NAME = 'demand'

    def __init__(self, result_mng, name, cfg=None, **kwargs):
        """Naming constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Actuator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping
        """
        if result_mng.result_name != self.DEFAULT_RESULT_NAME:
            self.log.warning(
                'Result name {} given to constructor does not correspond '
                'to {} to be estimated by {}'.format(
                    result_mng.result_name, self.DEFAULT_RESULT_NAME,
                    self.name))

        #: Climate-variable name.
        self.climate_variable = 'surface_temperature'
        #: Calendar-variable name.
        self.calendar_variable = 'calendar'

        # Initialize extractor and transformer
        super(Actuator, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg,
            variable_names=[self.climate_variable, self.calendar_variable],
            **kwargs)

        self.coef = {
            'daily_cycle_mean': None, 'regressor': None,
            'r2': None, 't_heat': None, 't_cool': None, 'alpha': None}

    def transform(self, data_src, stage=None, **kwargs):
        """Format temperature data from climate dataset.

        :param data_src: Input multiple data source containing climate
          and calendar data.
        :param stage: Modeling stage: `'fit'` or `'predict'`.
          May be required if features differ in the prediction stage.
        :type multidata_src: :py:class:`..data_source.MultiDataSource`
        :type stage: str

        :returns: Merged dataset.
        :rtype: :py:class:`xarray.Dataset`
        """
        # Get data sources
        clim_data_src = data_src.get_data_sources(self.climate_variable)
        cal_data_src = data_src.get_data_sources(self.calendar_variable)

        # Load climate data
        # Add regions domain cropping
        functions = [clim_data_src.crop_area]

        if hasattr(self.result_mng, 'modifier'):
            if (hasattr(self.result_mng.modifier.cfg, 'stage') and
                    (self.result_mng.modifier.cfg['stage'] != stage)):
                pass
            else:
                # Add modifier transformation
                functions.append(self.result_mng.modifier.transform)

        # Add get regional mean
        functions.append(clim_data_src.get_regional_mean)

        # Get temperature feature
        composer = Composer(*functions)

        ds_clim = clim_data_src.load(
            transform=composer, variable_names=self.climate_variable)

        # Convert from Kelvin to Celsius
        ds_clim[self.climate_variable] -= 273.15

        # Re-sample the climate data, if needed
        ds_clim = self._resample_data(ds_clim, reducer='mean', **kwargs)

        # Load calendar consistent with climate dataset
        ds_cal = cal_data_src.load(ds_clim.indexes['time'])

        # Return datasets merge
        return {**ds_clim, **ds_cal}

    def fit(self, data_src_in, data_src_out, **kwargs):
        """Learn statistical model of temperature-dependent demand
        and predict demand.

        :param data_src_in: Temperature and calendar dataset of training set.
        :param data_src_out: Demand dataset of training set.
        :type data_src_in: :py:class:`..data_source.DataSource`
        :type data_src_out: :py:class:`..data_source.DataSource`

        .. note::
          * This function uses grid search with k-fold cross validation to
            find the best heating/cooling temperature thresholds and
            regularization parameter.
          * These hyper-parameters are the same for all regions,
            so that the model has multiple outputs (one for each region)
            and the score for the cross valideation is given by the
            sum of the individual coefficients of determination for each region
            weighted by the fraction of the total variance explained by each
            region.
          * The feature matrix of the demand model is computed by calling the
            `fit` member function of the class
            :py:class:`DemandFeatureHeatCoolDays`, which itself calls
            the function :py:func:`_get_demand_feature_heat_cool_days`.

        """
        # Select component and result and reorder regions and coordinates
        da_clim = select_data(data_src_in, self.result_mng,
                              variable_name=self.climate_variable, **kwargs)
        da_cal = select_data(data_src_in, self.result_mng,
                             variable_name=self.calendar_variable, **kwargs)
        da_dem = select_data(data_src_out, self.result_mng, **kwargs)

        # Resample demand data, if needed
        da_dem = self._resample_data(da_dem, reducer='sum', **kwargs)

        # Assign variable coordinate
        da_clim = da_clim.expand_dims('variable').assign_coords(
            variable=[self.climate_variable])

        # Get common time index between demand and climate data
        da_clim, da_cal, da_dem = _select_time_slice(
            da_clim, da_cal, da_dem, **kwargs)

        # Get daily cycle mean
        if self.med.cfg['frequency'] == 'hour':
            self.coef['daily_cycle_mean'] = _get_daily_cycle(da_dem, da_cal)

        # Get raw design matrix
        des_mat_cycle = self._get_raw_design_matrix(da_clim, da_cal, **kwargs)

        # Cross-validation configuration
        if 'n_splits' in self.cfg:
            n_splits = self.cfg['n_splits']
        else:
            years = des_mat_cycle.indexes['time'].year
            n_splits = years[-1] - years[0] + 1
        # cv = TimeSeriesSplit(n_splits=self.cfg['n_splits'])
        cv = KFold(n_splits=n_splits)
        # scoring = 'neg_mean_squared_error'

        # Heating and cooling temperature grid
        t_heat_grid = np.arange(self.cfg['t_heat']['start'],
                                self.cfg['t_heat']['stop'],
                                self.cfg['t_heat']['step'])
        t_cool_grid = np.arange(self.cfg['t_cool']['start'],
                                self.cfg['t_cool']['stop'],
                                self.cfg['t_cool']['step'])

        # Estimator
        grid = {'feature__t_heat':  t_heat_grid,
                'feature__t_cool': t_cool_grid}
        params = {'fit_intercept': False, 'normalize': True}
        if 'max_iter' in self.cfg:
            params['max_iter'] = self.cfg['max_iter']
        if ((self.cfg['method'] == 'Ridge')
                | (self.cfg['method'] == 'Lasso')):
            alpha_grid = np.logspace(self.cfg['alpha']['start'],
                                     self.cfg['alpha']['stop'],
                                     self.cfg['alpha']['num'])
            grid.update({'regressor__estimator__alpha': alpha_grid})
            if self.cfg['method'] == 'Ridge':
                estimator = linear_model.Ridge(**params)
            elif self.cfg['method'] == 'Lasso':
                estimator = linear_model.Lasso(**params)
        elif self.cfg['method'] == 'BayesianRidge':
            estimator = linear_model.BayesianRidge(**params)

        # Make grid estimator
        daytype_index = np.unique(da_cal)
        feature = DemandFeatureHeatCoolDays(daytype_index=daytype_index)
        regressor = MultiInputRegressor(estimator)
        pipe = Pipeline(steps=[('feature', feature), ('regressor', regressor)])
        grid_cv = GridSearchCV(pipe, grid, cv=cv, verbose=0)

        # Fit model
        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Fitting model by {}'.format(self.cfg['method']))
        grid_cv.fit(des_mat_cycle, da_dem.values)
        self.coef['regressor'], self.coef['r2'] = (
            grid_cv.best_estimator_, grid_cv.best_score_)

        # Get parameters of best model
        params = self.coef['regressor'].get_params()
        self.coef['t_heat'], self.coef['t_cool'] = (
            params['feature__t_heat'], params['feature__t_cool'])
        if self.cfg['method'] != 'BayesianRidge':
            self.coef['alpha'] = params['regressor__estimator__alpha']

        # Print parameters and scores
        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Best overall score: {:.2f}'.format(self.coef['r2']))
            self.log.info('Heating temperature: {:.1f}'.format(
                self.coef['t_heat']))
            self.log.info('Cooling temperature: {:.1f}'.format(
                self.coef['t_cool']))
            if self.cfg['method'] != 'BayesianRidge':
                self.log.info('Regularization coefficient: {:.1f}'.format(
                    self.coef['alpha']))

    def predict(self, data_src_in, **kwargs):
        """Get regional demand prediction from fitted model.

        :param data_src_in: Input data source for prediction.
        :type data_src_in: :py:class:`..data_source.DataSource`

        :returns: Prediction dataset.
        :rtype: :py:class:`xarray.Dataset`
        """
        if self.coef['r2'] is None:
            raise NotFittedError(
                'This demand estimator instance has not been fitted yet')

        # Select component and result and reorder regions and coordinates
        da_clim = select_data(data_src_in, self.result_mng,
                              variable_name=self.climate_variable, **kwargs)
        da_cal = select_data(data_src_in, self.result_mng,
                             variable_name=self.calendar_variable, **kwargs)

        # Assign variable coordinate
        da_clim = da_clim.expand_dims('variable').assign_coords(
            variable=[self.climate_variable])

        # Get raw design matrix
        des_mat_cycle = self._get_raw_design_matrix(da_clim, da_cal, **kwargs)

        # Predict
        kwargs = ({'return_std': True} if self.cfg['method'] == 'BayesianRidge'
                  else {})
        pred = self.coef['regressor'].predict(des_mat_cycle, **kwargs)

        # Collect regional demand prediction
        ds_pred = xr.Dataset()
        coords = dict(des_mat_cycle.coords)
        coord_reg = ('region', des_mat_cycle.coords['region'])
        coord_time = ('time', coords['time'])
        if self.cfg['method'] == 'BayesianRidge':
            y_mean, y_std = pred
            # Add random perturbations to prediction drawn from
            # posterior distribution
            if self.med.cfg['frequency'] == 'hour':
                # Constant perturbations throughout the day
                y_pert_day = np.random.normal(loc=0., scale=y_std[::24])
                y_pert = np.empty(y_mean.shape)
                for ih in range(24):
                    y_pert[ih::24] = y_pert_day
            elif self.med.cfg['frequency'] == 'day':
                y_pert = np.random.normal(loc=0., scale=y_std)
            prediction = y_mean + y_pert

            # Add mean, standard deviation, alpha and lambda
            # y_mean = xr.DataArray(y_mean, coords=[coord_time, coord_reg],
            #                       name='demand_mean')
            y_std = xr.DataArray(y_std, coords=[coord_time, coord_reg],
                                 name='demand_std')
        else:
            prediction = pred

        # Add prediction
        prediction = xr.DataArray(prediction, coords=[coord_time, coord_reg])
        prediction.attrs['r2_total'] = self.coef['r2']
        prediction.attrs['t_heat'] = self.coef['t_heat']
        prediction.attrs['t_cool'] = self.coef['t_cool']
        if self.cfg['method'] != 'BayesianRidge':
            prediction.attrs['alpha'] = self.coef['alpha']

        # Add units
        if self.med.cfg['frequency'] == 'day':
            prediction.attrs['units'] = 'MWh/d'
        elif self.med.cfg['frequency'] == 'hour':
            prediction.attrs['units'] = 'MWh/h'
        ds_pred[self.result_mng.result_name] = prediction

        np.set_printoptions(precision=1)
        da_clim = des_mat_cycle.loc[{'variable': self.climate_variable}]
        val = prediction.mean('time').values * 365 / 1e6
        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Total fitted demand mean (TWh/y): {}'.format(val))
            if self.cfg['method'] == 'BayesianRidge':
                y_std *= 365 / 1e6
                val = np.sqrt((y_std**2).mean('time').values)
                self.log.info(
                    'Total fitted demand std (TWh/y): {}'.format(val))
            # Get number of heating and cooling days
            n_heating_days = (da_clim < self.coef['t_heat']).mean(
                'time').values * 365
            n_cooling_days = (da_clim > self.coef['t_cool']).mean(
                'time').values * 365
            self.log.info('Number of heating days per year: {}'.format(
                n_heating_days))
            self.log.info('Number of cooling days per year: {}'.format(
                n_cooling_days))

        return ds_pred

    def get_extractor_postfix(self, **kwargs):
        """Get postfix corresponding to wind features.

        returns: Postfix.
        rtype: str
        """
        postfix = '{}_{}'.format(
            super(Actuator, self).get_extractor_postfix(**kwargs),
            self.med.cfg['frequency'])

        return postfix

    def get_estimator_postfix(self, **kwargs):
        """Get estimator postfix.

        returns: Postfix.
        rtype: str
        """
        return '{}_{}'.format(
            super(Actuator, self).get_estimator_postfix(**kwargs),
            self.cfg['method'])

    def _resample_data(self, data, reducer=None, **kwargs):
        """Resample dataset, if needed.

        :param data: Data.
        :param reducer: Name of method used to reduce after resampling.
        :type data: :py:class:`xarray.Dataset` or :py:class:`xarray.DataArray`
        :type reducer: str

        :returns: Data.
        :rtype: :py:class:`xarray.Dataset` or :py:class:`xarray.DataArray`
        """
        freq_data = data.indexes['time'].inferred_freq.upper()
        if ((freq_data in ['H', '1H']) and
                (self.med.cfg['frequency'] == 'day')):
            # Resample
            gp = data.resample(time='D')

            # Apply reduction
            meth = getattr(gp, reducer)
            data = meth('time', keep_attrs=True)
        elif ((freq_data in ['D', '1D']) and
              (self.med.cfg['frequency'] == 'hour')):
            end_time = data.indexes['time'][-1] + pd.Timedelta(23, unit='H')
            th = pd.date_range(
                start=data.indexes['time'][0], end=end_time, freq='H')
            data = data.reindex(time=th).ffill('time')

        return data

    def _get_raw_design_matrix(self, da_clim, da_cal, **kwargs):
        """Get raw design matrix.

        :param da_clim: Climate-data array.
        :param da_cal: Calendar-data array.
        :type da_clim: :py:class:`xarray.DataArray`
        :type da_cal: :py:class:`xarray.DataArray`

        :returns: Raw design matrix.
        :rtype: :py:class:`xarray.DataArray`
        """
        # Apply daily_cycle
        daily_cycle_series = _apply_daily_cycle(
            da_cal, self.coef.get('daily_cycle_mean'),
            self.med.cfg['frequency'])

        # Concatenate results and make sure dimensions in right order
        _, daily_cycle_series = xr.broadcast(
            da_clim, daily_cycle_series, exclude=['time', 'variable'])
        des_mat_cycle = xr.concat(
            [da_clim, daily_cycle_series], dim='variable')
        des_mat_cycle = des_mat_cycle.transpose('time', 'variable', 'region')

        return des_mat_cycle


def _get_demand_feature_heat_cool_days(
        des_mat, daytype_index, t_heat, t_cool):
    """Get feature matrix of demand model with as variables heating
    and cooling temperature ramps and as factors week-days types.

    :param des_mat: Array containing climatic variables, i.e.
        mean temperature(Celsius),
        and membership of days to types 'work', 'sat' and 'off'
        (possibly including a daily cycle).
    :param daytype_index: Daytype index.
    :param t_heat: Temperature threshold below which consumers
        turn on heating.
    :param t_cool: Temperature threshold above which consumers
        turn on air conditionning.
    :type des_mat: py:class:`xarray.DataArray`
    :type daytype_index: sequence
    :type t_heat: float
    :type t_cool: float

    :returns: Feature matrix.
    :rtype: :py:class:`xarray.DataArray`
    """
    temp_label = 'surface_temperature'
    # Get variable labels
    piece_name = ['one', 'heat', 'cool']
    variable_names = np.concatenate(
        [[['{}_{}'.format(v, day)] for v in piece_name]
         for day in daytype_index])[:, 0]

    # Build feature array
    coords = dict(des_mat.coords.items())  # Copy dictionary of coordinates
    # Update variable coordinate
    coords['variable'] = variable_names
    coords = [(dim, coords[dim]) for dim in des_mat.dims]
    shape = [len(coord[1]) for coord in coords]
    feature = xr.DataArray(np.zeros(shape), coords=coords,
                           name='demand_feature_heat_cool_days')

    # Select temperature
    z = des_mat.sel(variable=temp_label, drop=True)

    for day in daytype_index:
        # Day type mask
        id_day = des_mat.sel(variable=day, drop=True)

        # Intercept for each
        feature.loc[{'variable': 'one_{}'.format(day)}] = id_day

        # Heating temperature
        feature.loc[{'variable': 'heat_{}'.format(day)}] = (
            (t_heat - z) * np.heaviside(t_heat - z, 0.)) * id_day
        # (z < t_heat).astype(float))

        # Cooling temperature
        feature.loc[{'variable': 'cool_{}'.format(day)}] = (
            (z - t_cool) * np.heaviside(z - t_cool, 0.)) * id_day
        # (z > t_cool).astype(float)

    # Transpose with regions (outputs) as last dimension
    feature = feature.transpose('time', 'variable', 'region')

    return feature


class DemandFeatureHeatCoolDays():
    """Class given to a scikit-learn pipeline to extract feature
    of the piecewise-linear_model of demand as a function of
    temperature and type of days."""

    def __init__(self, daytype_index, t_heat=12., t_cool=18.):
        """Constructor.

        :param daytype_index: Day-type index.
        :param t_heat: Heating-temperature threshold. Default is `12.`.
        :param t_cool: Cooling-temperature threshold. Default is `12.`.
        :type daytype_index: sequence
        :type t_heat: float
        :type t_cool: float
        """
        #: Heating-temperature threshold.
        self.t_heat = t_heat

        #: Cooling-temperature threshold.
        self.t_cool = t_cool

        #: Day-type index.
        self.daytype_index = daytype_index

    def fit(self, des_mat, y=None):
        """Fit doing nothing."""
        return self

    def transform(self, des_mat):
        """Transform by calling :py:func:`_get_demand_feature_heat_cool_days`.

        :param des_mat: Design matrix.
        :type des_mat: :py:class:`xarray.DataArray`

        :returns: Feature matrix.
        :rtype: :py:class:`xarray.DataArray`
        """
        return _get_demand_feature_heat_cool_days(
            des_mat, self.daytype_index, self.t_heat, self.t_cool)

    def set_params(self, t_heat=None, t_cool=None, daytype_index=None):
        """Mimick `set_params` method from scikit-learn.

        .. todo:: Inheritance from scikit-learn was removed due to
          metaclass conflict when generating sphinx doc.
          Find a better solution.
        """
        # Set heating parameters
        if t_heat is not None:
            self.t_heat = t_heat
        # Set cooling parameters
        if t_cool is not None:
            self.t_cool = t_cool
        # Set daytype_index parameters
        if daytype_index is not None:
            self.daytype_index = daytype_index

    def get_params(self, **kwargs):
        """Mimick `set_params` method from scikit-learn.

        .. todo:: Inheritance from scikit-learn was removed due to
          metaclass conflict when generating sphinx doc.
          Find a better solution.
        """
        return {'t_heat': self.t_heat, 't_cool': self.t_cool,
                'daytype_index': self.daytype_index}


def _get_daily_cycle(da_dem, da_cal):
    """Build an array of complementary columns corresponding
    to each day type of the calendar.
    Non-zero values are given by a composite hourly cycle given by
    the average of demand over all samples of same day type and hour.

    :param da_dem: Demand array.
    :param da_cal: Calendar array.
    :type da_dem: :py:class:`xarray.DataArray`
    :type da_cal: :py:class:`xarray.DataArray`

    :returns: Array with each column corresponding to a day type.
    :rtype: :py:class:`xarray.DataArray`
    """
    # Group by day type, and hour if needed
    hours = da_cal.indexes['time'].hour
    hours.name = 'hour'
    da_dem.coords['daytype_hour'] = (
        'time', pd.MultiIndex.from_arrays([da_cal, hours]))
    gp_daily_cycle = da_dem.groupby('daytype_hour')

    # Get time-mean daily cycle per day type
    daily_cycle_mean = gp_daily_cycle.mean('time')

    return daily_cycle_mean


def _apply_daily_cycle(da_cal, daily_cycle_mean=None, frequency='day'):
    """Build an array of complementary columns corresponding
    to each day type of the calendar. If frequency is `'day'`,
    non-zero values are unitary, else, if frequency is `'hour'`,
    non-zero values are given by a composite hourly cycle given by
    the average of demand over all samples of same day type and hour.

    :param da_cal: Calendar array.
    :param daily_cycle_mean: Mean daily cycle of output data.
      Default is `None`.
    :param frequency: Sampling frequency as either `'day'` or `'hour'`.
       Default is `'day'`.
    :type da_cal: :py:class:`xarray.DataArray`
    :type daily_cycle_mean: :py:class:`xarray.DataArray`
    :type frequency: str

    :returns: An array with each column corresponding to a day type.
    :rtype: :py:class:`xarray.DataArray`
    """
    # Initialize cycle
    time = da_cal.indexes['time']
    daytype_index = np.unique(da_cal)
    coords = [('time', time), ('variable', daytype_index)]
    daily_cycle_series = xr.DataArray(
        np.zeros((len(time), len(daytype_index))), coords=coords)

    # Group by day type, and hour if needed
    if frequency == 'hour':
        hours = time.hour
        hours.name = 'hour'
        grouper = 'daytype_hour'
        group_index = pd.MultiIndex.from_arrays([da_cal, hours])
        daily_cycle_series.coords[grouper] = ('time', group_index)

        # Group calendar by daytype and hours
        gp_out = daily_cycle_series.groupby(grouper)

        # Fill cycle with composite
        daily_cycle_series = gp_out + daily_cycle_mean

        # Drop group variable
        daily_cycle_series = daily_cycle_series.drop(grouper)
    elif frequency == 'day':
        # Group calendar by daytype
        gp_out = daily_cycle_series.groupby(da_cal)
        for gp_key, gp_idx in gp_out.groups.items():
            daily_cycle_series.loc[{'variable': gp_key}][gp_idx] = 1

    return daily_cycle_series


def _select_time_slice(da_clim, da_cal, da_dem, **kwargs):
    """Select time slice from common index.

    :param da_clim: Climate data array.
    :param da_cal: Calendar data array.
    :param da_dem: Demand data array.
    :type da_clim: :py:class:`xarray.DataArray`
    :type da_cal: :py:class:`xarray.DataArray`
    :type da_dem: :py:class:`xarray.DataArray`

    :returns: Time-sliced data.
    :rtype: :py:class:`tuple` containing three
      :py:class:`xarray.DataArray`
    """
    common_index = da_dem.indexes['time']
    common_index = common_index.intersection(da_clim.indexes['time'])
    time_slice = slice(common_index[0], common_index[-1])

    # Select time slice
    da_clim = da_clim.sel(time=time_slice)
    da_cal = da_cal.sel(time=time_slice)
    da_dem = da_dem.sel(time=time_slice)

    return da_clim, da_cal, da_dem
