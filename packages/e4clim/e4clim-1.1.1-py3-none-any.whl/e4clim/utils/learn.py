"""Statistical learning."""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import r2_score


class ShiftingBiasCorrector():
    """Bias corrector via shifting in order for the input and output
    means to coincide.
    """

    def __init__(self):
        """Constructor."""
        #: Intercept set when fitting.
        self.coef_ = None

    def fit(self, X, y):
        """Fit.

        :param X: Input data.
        :param y: output data.
        :type X: array_like
        :type y: array_like

        :returns: :py:obj:`self`.
        :rtype: :py:class:`ShiftingBiasCorrector`

        .. warning:: :py:obj:`X` and :py:obj:`y` should have the same
          dimensions.
        """
        self.coef_ = y.mean() - X.mean()

        return self

    def predict(self, X, return_std=False):
        """Predict multi-output variable using a model
            trained for each target variable.

        :param X: Input data.
        :type X: array_like

        :returns: Prediction.
        :rtype: array_like
        """
        return X + self.coef_

    def score(self, X, y):
        """r2 score.

        :param X: Input data.
        :param y: output data.
        :type X: array_like
        :type y: array_like

        :returns: r2 score.
        :rtype: float
        """
        return r2_score(y, self.predict(X))

    def get_params(self, deep=True):
        return {}

    def set_params(self, d):
        return self


class MultiInputRegressor():
    """Multi input estimator.

    :param estimator: An estimator implementing `fit` and `predict`.
    :type estimator: estimator object
    """

    def __init__(self, estimator):
        """Constructor.

        :param estimator: Estimator.
        :type estimator: :py:class:`sklearn.base.BaseEstimator`
        """
        #: Base estimator.
        self.estimator = estimator
        #: Multiple estimators.
        self.estimators = None
        #: Scores for each estimator.
        self.scores = None

    def fit(self, X, y):
        """Fit model to data.
        Fit a separate model for each input and output variables.

        :param X: Input array,
            shape(n_samples, n_feature, n_outputs).
        :param y: Output array, shape(n_samples, n_outputs)
        :type X: array_like
        :type y: array_like

        :returns: :py:obj:`self`
        :rtype: :py:class:`MultiInputRegressor`
        """
        # Loop over inputs and outputs
        self.estimators = []
        for ie, (X_l_T, y_l_T) in enumerate(zip(X.T, y.T)):
            # Clone estimator
            e = clone(self.estimator)

            # Fit data
            e.fit(X_l_T.T, y_l_T.T)

            # Save estimator
            self.estimators.append(e)

        # Save number of estimators
        self.n_estimators = len(self.estimators)

        return self

    def predict(self, X, return_std=False):
        """Predict multi-output variable using a model
            trained for each target variable.

        :param X: Input data, shape(n_samples, n_feature, n_outputs).
        :param return_std: If `True`, return standard deviation
           of posterior prediction(in the Bayesian case).
           Default is `False`.
        :type X: array_like
        :type return_std: bool

        :returns: Prediction.
        :rtype: array_like
        """
        y_pred = np.empty((X.shape[0], X.shape[2]))
        if return_std:
            y_std = np.empty((X.shape[0], X.shape[2]))
        for ie, X_l_T in enumerate(X.T):
            # Manage return std for Bayesian case only
            kwargs = {'return_std': True} if return_std else {}

            # Predict
            pred = self.estimators[ie].predict(X_l_T.T, **kwargs)

            # Manage prediction result
            if return_std:
                y_pred[:, ie] = pred[0]
                y_std[:, ie] = pred[1]
            else:
                y_pred[:, ie] = pred
        if return_std:
            return (y_pred, y_std)
        else:
            return y_pred

    def score(self, X, y):
        """Compute individual scores and variance-weighted score
        of multiple-output prediction.

        :param X: Input data, shape(n_samples, n_feature, n_outputs).
        :param y: True target data, shape(n_samples, n_outputs).
        :type X: array_like
        :type y: array_like

        :returns: Variance-weighted score.
        :rtype: float

        .. note:: Individual scores are saved in :py:attr:`scores`.
        """
        # Predict
        y_pred = self.predict(X)

        # Save raw scores
        self.scores = r2_score(y, y_pred, multioutput='raw_values')

        # Return variance weighted score
        score = (self.scores * y.var(0)).sum() / y.var(0).sum()

        return score


def last_full_years_date(time, first_date, **kwargs):
    """Get last date in date-time index which is a multiple of a year
    away from start date.

    :param time: Date-time index.
    :param first_date: First date.
    :type time: :py:class:`pandas.DatetimeIndex`
    :type first_date: :py:class:`datetime.date`

    :returns: Last date.
    :rtype: :py:class:`datetime.date`
    """
    last_date = pd.date_range(time[0], time[-1], freq='A-DEC')[-1]

    # Make sure last samples are present
    freq = time.inferred_freq
    if freq is None:
        if (time[1] - time[0]).seconds == 3600:
            freq = 'H'
    if freq == 'H':
        last_date += pd.Timedelta('23H')

    return last_date


def intersection_time_slice(da_in, da_out):
    """Get full years intersection between two arrays, if possible.

    :param da_in: First array.
    :param da_out: Second array.
    :type da_in: :py:class:`xarray.DataArray`
    :type da_out: :py:class:`xarray.DataArray`

    :returns: Intersection time slice.
    :rtype: slice

    .. warning:: The time index of the input and output arrays
      must be compatible. For instance, daily-sampled indices
      but with different hours won't intersect.
    """
    # Match frequencies
    t_out = da_out.indexes['time']
    freq_out = t_out.inferred_freq
    t_in = da_in.indexes['time']
    freq_in = t_in.inferred_freq
    if freq_out in ['A-DEC', 'Y']:
        # Make index of yearly mean start 1st of January
        da_out['time'] = pd.DatetimeIndex(
            ['{}-01-01'.format(t.year) for t in t_out])
        if freq_in == 'H':
            start = '{}-01-01 00:00:00'.format(t_out[0].year)
            end = '{}-12-31 23:00:00'.format(t_out[-1].year)
            t_out_hour = pd.date_range(start, end, freq=freq_in)
            da_out = da_out.reindex(time=t_out_hour, method='ffill')

    t_inter = da_out.indexes['time'].intersection(
        da_in.indexes['time'])
    if len(t_inter) > 0:
        first_date_inter = t_inter[0]
        last_date_inter = last_full_years_date(
            t_inter, first_date_inter)
        if ((last_date_inter - first_date_inter)
                >= pd.Timedelta(1, unit='Y')):
            # If there are at least a year of common data,
            # use common data only
            time_slice = slice(first_date_inter, last_date_inter)

            return time_slice


def parse_fit_data(
        data_src_in, data_src_out, result_mng, subsample_freq=None,
        select_period=False, time_slice=None, **kwargs):
    """Get input and output data arrays.

    :param data_src_in: Training set input data source.
    :param data_src_out: Training set output data source.
    :param result_mng: Result manager.
    :param subsample_freq: Sub-sampling frequency. Default is `None`, in which
      case no sub-sampling is performed.
    :param time_slice: Time slice to select period. Default is `None` in which
      case the full period is kept.
    :param select_period: Whether to select period. Default is `False`.
    :type data_src_in: :py:class:`..data_source.DataSourceBase`
    :type data_src_out: :py:class:`..data_source.DataSourceBase`
    :type result_mng: :py:class:`..component.ResultManager`
    :type subsample_freq: str
    :type select_period: bool
    :type time_slice: slice

    :returns: Input and output data arrays.
    :rtype: :py:class:`tuple` containing two
      :py:class:`xarray.DataArray`'s
    """
    # Select result, copy and ensure dimensions order
    da_in = select_data(data_src_in, result_mng, **kwargs)
    da_out = select_data(data_src_out, result_mng, **kwargs)

    # Subsample if requested
    if subsample_freq:
        da_in = da_in.resample(time=subsample_freq).mean('time')
        da_out = da_out.resample(time=subsample_freq).mean('time')

    if select_period:
        # Select input and output periods
        # as given by configuration or first full years
        da_in, time_slice = select_period_from_array(
            da_in, time_slice=time_slice, **kwargs)
        da_out, _ = select_period_from_array(
            da_out, time_slice=time_slice, **kwargs)

    return da_in, da_out


def select_period_from_array(da, time_slice=None, **kwargs):
    """Select full years period from an array.
    Try to get first and last dates from configuration.
    Otherwise, select the first full years.

    :param da: Array.
    :param time_slice: Time slice to select period. Default is `None` in which
      case the full period is kept.
    :type da: :py:class:`xarray.DataArray`
    :type time_slice: :py:class:`slice` or collection

    :returns: Tuple containing the selected array and time slice.
    :rtype: :py:class:`tuple` of :py:class:`xarray.DataArray`
      and :py:class:`slice`
    """
    if time_slice is None:
        # Get time index
        time = da.indexes['time']

        # First date is given or first available date
        first_date = pd.Timestamp(time[0])

        # Last date is given or last date which is a multiple of one
        # year past first date
        last_date = pd.Timestamp(
            last_full_years_date(time, first_date, **kwargs))
    else:
        try:
            first_date, last_date = time_slice.start, time_slice.stop
        except AttributeError:
            first_date, last_date = time_slice

    # Slice
    time_slice = slice(first_date, last_date)
    da = da.sel(time=time_slice)

    return da, time_slice


def select_data(data_src, result_mng, variable_name=None, **kwargs):
    """Select variable from data source, copy it, reorder regions,
    drop components and transpose, if possible.

    :param data_src: Training set input data source.
    :param result_mng: Result manager.
    :param variable_name: Variable to select from data source.
      Default is `None`, in which case `result_mng.result_name`
      is used instead.
    :type data_src: :py:class:`..data_source.DataSourceBase`
    :type result_mng: :py:class:`..component.ResultManager`
    :type variable_name: str

    :returns: Input and output data arrays.
    :rtype: :py:class:`tuple` containing two
      :py:class:`xarray.DataArray`'s
    """
    component_mng = result_mng.component_mng

    # Select variable or result
    variable_name = variable_name or result_mng.result_name
    da = data_src[variable_name].copy(deep=True)

    # Try to reorder regions from component-manager place names
    try:
        da = da.sel(region=component_mng.place_names)
    except ValueError:
        pass

    # Try to select component in case needed
    try:
        da = da.sel(component=component_mng.component_name, drop=True)
    except ValueError:
        pass
    try:
        da = da.drop('component')
    except ValueError:
        pass

    # Try to transpose
    try:
        da = da.transpose('time', 'region')
    except ValueError:
        pass

    return da
