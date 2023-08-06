"""Estimator of capacity factor time series from generation time series
and capacity factor averages."""
import numpy as np
import pandas as pd
from ..actuator_base import ExtractorBase
from ..utils.learn import select_data


class Actuator(ExtractorBase):
    """Estimator of capacity factor time series from generation time series
    and capacity factor averages."""
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
        if result_mng.result_name != self.DEFAULT_RESULT_NAME:
            self.log.warning(
                'Result name {} given to constructor does not correspond '
                'to {} to be estimated by {}'.format(
                    result_mng.result_name, self.DEFAULT_RESULT_NAME,
                    self.name))

        super(Actuator, self).__init__(
            result_mng=result_mng, name=name, cfg=cfg,
            variable_names={result_mng.result_name, 'capacity'}, **kwargs)

        #: Required input-variables.
        self.input_variable_names = set(['generation', 'capacity_factor'])

    def transform(self, data_src, **kwargs):
        """Extract capacity factor time series from generation time series
        and capacity factor averages for component.

        :param data_src: Input data source containing generation
          time series and capacity factor averages.
        :type data_src: :py:class:`.data_source.DataSourceBase`

        :returns: Capacity factor and capacity time series.
        :rtype: :py:class:`dict` from :py:class:`str` to
          :py:class:`xarray.DataArray`
        """
        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Computing {} {} time series from {} generation time series '
                'and {} capacity factor means'.format(
                    self.component_mng.name, self.result_mng.name,
                    *list(data_src.var_data_sources['generation']),
                    *list(data_src.var_data_sources['capacity_factor'])))

        # Get data (letting multiple data source manage variables)
        kwargs_data_src = kwargs.copy()
        kwargs_data_src.pop('variable_names', None)
        data_src.get_data(**kwargs_data_src)

        # Select component and result and reorder regions and coordinates
        da_gen = select_data(data_src, self.result_mng,
                             variable_name='generation', **kwargs)
        da_cf_mean = select_data(data_src, self.result_mng,
                                 variable_name='capacity_factor', **kwargs)

        # Get mean generation
        da_gen_mean = da_gen.resample(
            time=self.cfg['mean_frequency']).mean('time')

        # Get mean capacity factor, thus making sure that
        # to down-sample if needed and to use the same
        # time-index format as for the generation
        da_cf_mean = da_cf_mean.resample(
            time=self.cfg['mean_frequency']).mean('time')

        # Get mean capacity
        da_cap_mean = da_gen_mean / da_cf_mean

        # # Get capacity time series by linearly interpolating
        # da_cap = da_cap_mean.resample(time='H').interpolate('linear')

        t_cap_mean = da_cap_mean.indexes['time']
        start = '{}-01-01'.format(t_cap_mean[0].year)
        # # Get capacity time series from last year to avoid 2015
        # # high generation
        # start = '{}-01-01'.format(t_cap_mean[0].year + 1)
        end = t_cap_mean[-1] + pd.Timedelta(23, unit='H')
        t_sub = pd.date_range(start=start, end=end, freq='H')
        da_cap = da_cap_mean.reindex(time=t_sub).bfill('time').ffill('time')

        # Get capacity factors time series on intersection
        da_cf_sub = da_gen / da_cap

        if self.cfg.get('extrapolate'):
            da_cf = _extrapolate(da_cf_mean, da_cf_sub, **kwargs)
        else:
            da_cf = da_cf_sub

        # Format
        da_cf.name = self.result_mng.result_name
        da_cf.attrs['units'] = ''
        da_cap_mean.name = 'capacity'

        return {da_cf.name: da_cf, da_cap_mean.name: da_cap_mean}

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        postfix = '{}_{}'.format(
            super(Actuator, self).get_extractor_postfix(**kwargs),
            self.med.cfg['frequency'])

        if self.cfg.get('extrapolate'):
            postfix += '_extrapolate'

        return postfix


def _extrapolate(da_mean, da_sub, time_name='time', **kwargs):
    """Extrapolate hourly data to years for which not hourly
    data is available by multiplying the mean hourly profile over
    a year by the yearly-mean data for which more years are available.

    :param da_mean: Time-averaged data array.
    :param da_sub: Data array over non-extrapolated period.
    :param time_name: Time-dimension name. Default is `time`.
    :type da_mean: :py:class:`xarray.DataArray`
    :type da_sub: :py:class:`xarray.DataArray`
    :type time_name: str

    :returns: Extrapolated data array.
    :rtype: :py:class:`xarray.DataArray`

    .. warning:: Time index should start with new year.
    """
    t_mean = da_mean.indexes[time_name]
    start = '{}-01-01'.format(t_mean[0].year)
    end = t_mean[-1] + pd.Timedelta(23, unit='H')
    t_ext = pd.date_range(start=start, end=end, freq='H')
    t_sub = da_sub.indexes[time_name]
    da = da_sub.reindex(**{time_name: t_ext})
    da = _filter_leap_years(da, time_name=time_name)

    # Get year to use to extrapolate
    da_cycle = da.sel(**{time_name: str(t_sub[0].year)})

    # Compute correctors for each year based on yearly mean
    corrector = da_mean / da_sub.mean(time_name)

    # Apply correction to missing years
    gp = da.resample(**{time_name: 'Y'})
    for date, da_date in gp:
        # Time index of year
        date = pd.Timestamp(date)
        t_date = da_date.indexes[time_name]

        # Add year only if absent
        if date.year not in t_sub.year:
            # Correct year
            da_corr = da_cycle * corrector.sel(**{time_name: date}, drop=True)

            # Add year
            da_corr[time_name] = (time_name, t_date)
            da.loc[{time_name: str(date.year)}] = da_corr

    return da


def _filter_leap_years(da, time_name='time', **kwargs):
    """Remove additional days from leap years.

    :param da: Data array from which to remove days.
    :param time_name: Time-dimension name. Default is `time`.
    :type da: :py:class:`xarray.DataArray`
    :type time_name: str

    :returns: Filtered data array.
    :rtype: :py:class:`xarray.DataArray`
    """
    t = da.indexes[time_name]
    leap_years = np.unique(t.year[t.is_leap_year])
    da_filt = da.copy(deep=True)
    for year in leap_years:
        sy = '{}-02-29'.format(year)
        da_filt = da_filt[(da_filt.indexes[time_name].date !=
                           pd.Timestamp(sy).date())]

    return da_filt
