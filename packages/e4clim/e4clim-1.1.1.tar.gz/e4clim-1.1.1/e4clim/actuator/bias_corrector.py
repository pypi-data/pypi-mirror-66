"""Bias corrector and predictor."""
import operator
from numpy import set_printoptions
import pandas as pd
from sklearn.exceptions import NotFittedError
from ..actuator_base import EstimatorBase
from ..utils.learn import parse_fit_data, select_data


class Actuator(EstimatorBase):
    """Bias corrector and predictor."""

    def __init__(self, result_mng, name, cfg=None, **kwargs):
        """Naming constructor.

        :param result_mng: Result manager of variable to estimate.
        :param name: Actuator name.
        :param cfg: Actuator configuration. Default is `None`.
        :type result_mng: :py:class:`ResultManager`
        :type name: str
        :type cfg: mapping
        """
        super(Actuator, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg,
            **kwargs)

        #: Operator choice.
        self._operator_choice = self.cfg.get('operator')
        self._operator_choice = ('scale' if self._operator_choice is None
                                 else self._operator_choice)

        #: Bias-correction operator.
        #: Set to :py:meth:`operator.mul`, or :py:meth:`operator.add`,
        #: if :py:attr:`_operator_choice` is `'scale'`, or `'shift'`,
        #: respectively.
        self._operator = None

        #: Inverse of bias-correction operator
        #: Set to :py:meth:`operator.truediv`, or :py:meth:`operator.sub`,
        #: if :py:attr:`_operator_choice` is `'scale'`, or `'shift'`,
        #: respectively.
        self._operator_inv = None

        if self._operator_choice == 'scale':
            self._operator = operator.mul
            self._operator_inv = operator.truediv
        elif self._operator_choice == 'shift':
            self._operator = operator.add
            self._operator_inv = operator.sub

    def fit(self, data_src_in, data_src_out, **kwargs):
        """Get bias corrector for component as a factor to multiply the
        input data with and such that the training input data
        multiplied by the bias corrector has the same mean
        as the training output data over the same period.

        :param data_src_in: Training set input data source.
        :param data_src_out: Training set output data source.
        :type data_src_in: :py:class:`.data_source.DataSourceBase`
        :type data_src_out: :py:class:`.data_source.DataSourceBase`

        .. warning:: If the `intersection_only_if_possible` entry of the
          container configuration is `True`, an attempt is made to
          compute the bias on a common time-slice. The time indices of
          the two data sources should, however, be compatible.

        .. seealso:: :py:func:`_intersection_time_slice`
        """
        # Get input and output data arrays
        da_in, da_out = parse_fit_data(
            data_src_in, data_src_out, self.result_mng,
            subsample_freq=self.cfg.get('subsample_freq'),
            select_period=True, time_slice=self.cfg.get('time_slice'),
            **kwargs)

        # Check if selected period intersects that of input period
        time_slice_in = slice(*da_in.indexes['time'][[0, -1]])
        time_slice_out = slice(*da_out.indexes['time'][[0, -1]])
        if self.cfg.get('intersection_only_if_possible'):
            inter_slice = _intersection_time_slice(da_in, da_out)
            if inter_slice is not None:
                time_slice_in = time_slice_out = inter_slice

        # Get bias corrector
        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Computing {} {} bias corrector from {} to {} (input) '
                'and from {} to {} (output)'.format(
                    self.result_mng.name, self.component_mng.name,
                    time_slice_in.start, time_slice_in.stop,
                    time_slice_out.start, time_slice_out.stop))
        mean_in = da_in.sel(time=time_slice_in).mean('time')
        mean_out = da_out.sel(time=time_slice_out).mean('time')
        bc = self._operator_inv(mean_out, mean_in)

        # Convert coordinates datatypes from object to str if needed
        for dim in bc.dims:
            if bc[dim].dtype == object:
                bc[dim] = bc[dim].astype(str)
        self.coef = bc

        set_printoptions(precision=3)
        if not self.cfg.get('no_verbose'):
            self.log.info('Computed average ({} / {}):'.format(
                time_slice_in.start, time_slice_in.stop))
            self.log.info(mean_in.values)
            self.log.info('Observed average ({} / {}):'.format(
                time_slice_out.start, time_slice_out.stop))
            self.log.info(mean_out.values)

    def predict(self, data_src_in, **kwargs):
        """Apply bias corrector for component by multipling input data.

        :param data_src_in: Input data source.
        :type data_src_in: :py:class:`..data_source.DataSourceBase`

        :returns: Bias corrected dataset.
        :rtype: dict
        """
        ds = {}
        # Verify that bias corrector has been fitted
        if self.coef is None:
            raise NotFittedError('This bias corrector instance '
                                 'must be fitted before prediction.')

        # Select result, copy and ensure dimensions order
        da_in = select_data(data_src_in, self.result_mng, **kwargs)

        # Copy input dataset
        da_pred = da_in.copy(deep=True)

        # Reorder regions to comply
        coef_comp = (self.coef.loc[{'region': da_in.indexes['region']}]
                     if 'region' in self.coef.coords else self.coef.copy())

        # Select component if needed
        try:
            coef_comp = coef_comp.sel(
                component=self.component_mng.component_name)
        except ValueError:
            pass

        # Apply bias corrector, with input data
        da_pred = self._operator(da_pred, coef_comp)

        # Add bias-corrected output variable to dataset
        ds[self.result_mng.result_name] = da_pred

        return ds

    def _select_period_from_array(self, da, data_type):
        """Select full years period from an array.
        Try to get first and last dates from configuration.
        Otherwise, select the first full years.

        :param da: Array.
        :param data_type: `'in'` or '`out`' data type for which
          to get dates in configuration.
        :type da: :py:class:`xarray.DataArray`
        :type data_type: str

        :returns: Tuple containing the selected array and time slice.
        :rtype: :py:class:`tuple` of :py:class:`xarray.DataArray`
          and :py:class:`slice`
        """
        time_slice = self.cfg.get('{}_time_slice'.format(data_type))
        if time_slice is None:
            # Get time index
            time = da.indexes['time']

            # First date is given or first available date
            first_date = pd.Timestamp(
                self.cfg.get('first_date_{}'.format(data_type)) or
                time[0])

            # Last date is given or last date which is a multiple of one
            # year past first date
            last_date = pd.Timestamp(
                self.cfg.get('last_date_{}'.format(data_type)) or
                _last_full_years_date(time, first_date))
        else:
            first_date, last_date = time_slice

        # Slice
        time_slice = slice(first_date, last_date)
        da = da.sel(time=time_slice)

        return da, time_slice

    def get_estimator_postfix(self, **kwargs):
        """Get bias-corrector postfix.

        returns: Postfix.
        rtype: str
        """
        return '{}_nobias'.format(
            super(Actuator, self).get_estimator_postfix(**kwargs))


def _last_full_years_date(time, first_date):
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


def _intersection_time_slice(da_in, da_out):
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
        last_date_inter = _last_full_years_date(
            t_inter, first_date_inter)
        if ((last_date_inter - first_date_inter)
                >= pd.Timedelta(1, unit='Y')):
            # If there are at least a year of common data,
            # use common data only
            time_slice = slice(first_date_inter, last_date_inter)

            return time_slice
