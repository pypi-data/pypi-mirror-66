"""Bias corrector and predictor."""
from numpy import set_printoptions
import numpy as np
import xarray as xr
from sklearn.exceptions import NotFittedError
from sklearn import linear_model
from ..actuator_base import EstimatorBase
from ..utils.learn import parse_fit_data, select_data

REGRESSOR = linear_model.RidgeCV


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

    def fit(self, data_src_in, data_src_out, **kwargs):
        """Get bias corrector for component as a factor to multiply the
        input data with and such that the training input data
        multiplied by the bias corrector has the same mean
        as the training output data over the same period.

        :param data_src_in: Training set input data source.
        :param data_src_out: Training set output data source.
        :type data_src_in: :py:class:`..data_source.DataSourceBase`
        :type data_src_out: :py:class:`..data_source.DataSourceBase`
        """
        # Get input and output data arrays
        da_in, da_out = parse_fit_data(
            data_src_in, data_src_out, self.result_mng,
            subsample_freq=self.cfg.get('subsample_freq'),
            select_period=True, time_slice=self.cfg.get('time_slice'),
            **kwargs)

        # Select intersection
        t_in = da_in.indexes['time']
        t_intersect = t_in.intersection(da_out.indexes['time'])
        da_in = da_in.sel(time=t_intersect)
        da_out = da_out.sel(time=t_intersect)

        # Select valid
        valid = ~da_in.isnull() & ~da_out.isnull()
        da_in = da_in.where(valid, drop=True)
        da_out = da_out.where(valid, drop=True)

        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Computing {} {} bias corrector from {} to {} '.format(
                    self.result_mng.name, self.component_mng.name,
                    *da_in.indexes['time'][[0, -1]]))

        # Make multiple regional models into one model
        X = _get_factorized_input(da_in, **kwargs)
        y = _get_factorized_output(da_out, **kwargs)

        # Configure regression
        regressor_kwargs = self.cfg.get('regressor_kwargs') or {}

        if 'cv' not in regressor_kwargs:
            # Split by year for cross validation
            years = da_in.indexes['time'].year
            regressor_kwargs['cv'] = years.max() - years.min() + 1

        # Prevent fitting intercept
        regressor_kwargs['fit_intercept'] = False

        if 'alphas' not in regressor_kwargs:
            # Define regularization path from given logspace parameters
            alphas_logspace = self.cfg.get('alphas_logspace')
            if alphas_logspace is not None:
                alphas = np.logspace(**alphas_logspace)
                regressor_kwargs['alphas'] = alphas

        # Define regressor
        reg = REGRESSOR(**regressor_kwargs)

        # Ridge regression with cross validation
        reg.fit(X, y)

        # Get score
        score = reg.score(X, y)

        # Save coefficients
        try:
            coords = [da_in.region]
        except AttributeError:
            coords = []
        self.coef = xr.DataArray(reg.coef_, coords=coords, name='coef')
        self.coef.attrs['score'] = score
        self.coef.attrs['cv'] = regressor_kwargs['cv']
        try:
            self.coef.attrs['alpha'] = reg.alpha_
            self.coef.attrs['alphas'] = reg.alphas_
        except AttributeError:
            pass

        if not self.cfg.get('no_verbose'):
            set_printoptions(precision=3)
            self.log.info('Scale regression coefficients:')
            self.log.info(self.coef)

    def predict(self, data_src_in, **kwargs):
        """Apply bias corrector for component by multipling input data.

        :param data_src_in: Input data source.
        :type data_src_in: :py:class:`..data_source.DataSourceBase`

        :returns: Bias corrected dataset.
        :rtype: dict
        """
        # Verify that bias corrector has been fitted
        if self.coef is None:
            raise NotFittedError('This bias corrector instance '
                                 'must be fitted before prediction.')

        # Select result, copy and ensure dimensions order
        da_in = select_data(data_src_in, self.result_mng, **kwargs)

        # Reorder regions to comply
        coef_comp = (self.coef.loc[{'region': da_in.indexes['region']}]
                     if 'region' in self.coef.coords else self.coef.copy())

        # Select component if needed
        try:
            coef_comp = coef_comp.sel(
                component=self.component_mng.component_name)
        except ValueError:
            pass

        # Define regressor with previously fitted coefficients
        regressor_kwargs = self.cfg['regressor_kwargs'] or {}

        # Prevent fitting intercept
        regressor_kwargs['fit_intercept'] = False

        reg = REGRESSOR(**regressor_kwargs)
        reg.intercept_ = 0.

        # Set fitted coefficients
        reg.coef_ = self.coef.values

        # Initialize prediction depending on input dimensions
        if len(da_in.shape) > 1:
            da_pred = xr.full_like(
                da_in.stack(stacked_dim=['region', 'time']), None)
        else:
            da_pred = xr.full_like(da_in, None)

        # Get factorized input
        X = _get_factorized_input(da_in, **kwargs)

        # Predict
        da_pred[:] = reg.predict(X)

        # Unstack, if needed
        if len(da_in.shape) > 1:
            da_pred = da_pred.unstack('stacked_dim').transpose(
                'time', 'region')

        return {self.result_mng.result_name: da_pred}

    def get_estimator_postfix(self, **kwargs):
        """Get bias-corrector postfix.

        returns: Postfix.
        rtype: str
        """
        return '{}_scaled'.format(
            super(Actuator, self).get_estimator_postfix(**kwargs))


def _get_factorized_input(da_in, **kwargs):
    """Get input matrix factorized over regions.

    :param da_in: Input matrix.
    :type da_in: :py:class:`xarray.DataArray`

    :returns: Factorized input matrix.
    :rtype: :py:class:`numpy.ndarray`
    """
    shape = da_in.shape
    if len(shape) == 1:
        X = da_in.values
    else:
        nt, nreg = shape
        X = np.zeros((nt * nreg, nreg))
        for ir in range(nreg):
            # Set block of rows and column corresponding to region
            sl = slice(ir * nt, (ir + 1) * nt)

            # Linear
            X[sl, ir] = da_in.isel(region=ir).values

    return X


def _get_factorized_output(da_out, **kwargs):
    """Get output vector factorized over regions.

    :param da_out: Output matrix.
    :type da_out: :py:class:`xarray.DataArray`

    :returns: Factorized output vector.
    :rtype: :py:class:`numpy.ndarray`
    """
    if len(da_out.shape) == 1:
        # Return values
        y = da_out.values
    else:
        # Stack blocks of rows associated to each region
        y = da_out.stack(stacked_dim=['region', 'time'])

    return y
