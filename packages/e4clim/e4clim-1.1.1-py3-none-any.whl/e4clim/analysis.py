"""Various analysis functions."""
import os
import numpy as np
import pandas as pd
import xarray as xr
from scipy.stats import t
from uncertainties.unumpy import uarray


def get_band_spectrum(med, region=None, component_mng_names=None,
                      comp_time_slices={}, **kwargs):
    """Get band spectrum, i.e. the integration of power spectrum over
    frequency bands.

    :param med: Mediator.
    :param region: Region to select, `global` or `None`.
      Default is `None`, in which case all regions are kept.
      If `'global'`, data is aggregated over regions.
    :param component_mng_names: Names of components to select.
      Default is `None`, in which case all components in mediator are selected.
    :param comp_time_slices: Time slice per component.
    :type med: :py:class:`.mediator.Mediator`
    :type region: str
    :type component_mng_names: collection
    :type comp_time_slices: :py:class:`slice`-valued mutable

    :returns: Original and filtered datasets per component and result.
    :rtype: :py:class:`tuple` of mappings
    """
    freqs = ['Y', 'D', 'H']
    ds = {}
    var_tot = {}
    filt = {}
    var_filt = {}

    # Read hourly capacity factors from ENTSO-E and GSE
    component_mng_names = component_mng_names or med.component_managers.keys()
    for component_mng_name in component_mng_names:
        # Get result
        component_mng = med.component_managers[component_mng_name]
        file_dir = med.cfg.get_project_data_directory(component_mng, **kwargs)
        time_slice = (None if comp_time_slices is None else
                      comp_time_slices.get(component_mng_name))

        ds[component_mng_name] = {}
        var_tot[component_mng_name] = {}
        filt[component_mng_name] = {}
        var_filt[component_mng_name] = {}
        for result_mng_name, result_mng in (
                component_mng.result_managers.items()):
            # Get array for result and component
            da = result_mng.get_data()[result_mng_name]
            try:
                da = da.sel(component=result_mng.result_name)
            except ValueError:
                pass

            # Select time slice if needed
            if time_slice is not None:
                da = da.sel(time=time_slice)

            coords = [('frequency', freqs)]
            coords_shape = (len(freqs),)
            if region is not None:
                # Select region
                da = (da.sum('region', keep_attrs=True) if region == 'global'
                      else da.sel(region=region))
            else:
                coords.append(da.coords['region'])
                coords_shape += (len(da.coords['region']),)
            ds[component_mng_name][result_mng_name] = da

            # Get the total variance of each result
            da_var_tot = da.var('time')
            var_tot[component_mng_name][result_mng_name] = da_var_tot

            # Loop over the sampling frequencies
            high_pass = da.copy(deep=True)
            med.log.info('Filtering {}'.format(component_mng_name))
            filt_freq = {}
            filt[component_mng_name][result_mng_name] = filt_freq
            da_var_filt = xr.DataArray(np.zeros(coords_shape), coords=coords)
            var_filt[component_mng_name][result_mng_name] = da_var_filt
            for freq in freqs:
                med.log.info('- Frequency: {}'.format(freq))
                if freq != 'H':
                    # Low-pass filter
                    low_pass = high_pass.resample(time=freq).mean('time')
                    # Up-sample
                    t = low_pass.indexes['time']
                    if freq == 'Y':
                        low_pass = low_pass.reindex(
                            time=high_pass.indexes['time'],
                            method='bfill').ffill('time')
                    else:
                        new_index = pd.to_datetime({
                            'year': t.year, 'month': t.month, 'day': t.day,
                            'hour': 0.})
                        low_pass = low_pass.reindex(time=new_index)
                        low_pass = low_pass.reindex(
                            time=high_pass.indexes['time'], method='ffill')
                    # High-pass filter
                    high_pass -= low_pass
                else:
                    low_pass = high_pass

                # Store filtered data
                filt_freq[freq] = low_pass

                # Get the variance
                da_var_filt.loc[freq] = low_pass.var('time')

            # Get normalized variance
            da_var_filt_norm = da_var_filt / da_var_tot

            # Write result
            da_var_filt.attrs['units'] = str(da.attrs.get('units')) + '^2'
            da_var_filt_norm.attrs['units'] = ''
            da_var_tot.attrs['units'] = str(da.attrs.get('units')) + '^2'
            result_postfix = result_mng.get_data_postfix(**kwargs)
            # Write spectrum
            filename = 'band_spectrum_{}{}.nc'.format(
                result_mng.name, result_postfix)
            filepath = os.path.join(file_dir, filename)
            med.log.info('Writing {} {} variance and band spectrum to '
                         '{}'.format(component_mng_name, result_mng_name,
                                     filepath))
            xr.Dataset({'variance': da_var_tot,
                        'band_spectrum': da_var_filt,
                        'band_spectrum_normalized': da_var_filt_norm
                        }).to_netcdf(filepath)

    # Print results
    prec = 1
    np.set_printoptions(precision=prec)
    med.log.info('Component\tVariable\tFrequency Range\tVariance (%)')
    for component_mng_name in component_mng_names:
        component_mng = med.component_managers[component_mng_name]
        for result_mng_name in component_mng.result_managers.keys():
            for freq in freqs:
                val = var_filt[component_mng_name][result_mng_name].loc[
                    freq].values * 100
                med.log.info('{}\t{}:'.format(component_mng_name, freq))
                med.log.info(val)

    med.log.info('Component\tVariable\tFrequency Range\t'
                 'Standard Deviation (%)')
    for component_mng_name in component_mng_names:
        component_mng = med.component_managers[component_mng_name]
        for result_mng_name in component_mng.result_managers.keys():
            for freq in freqs:
                val = xr.ufuncs.sqrt(
                    var_filt[component_mng_name][result_mng_name].loc[
                        freq].values) * 100
                med.log.info('{}\t{}:'.format(component_mng_name, freq))
                med.log.info(val)

    return (ds, filt)


def compare_yearly_covariance(med_ref, med_new, component_mng_names=None,
                              **kwargs):
    dim_comp_reg_name = 'component_region'

    # Read hourly capacity factors from ENTSO-E and GSE
    component_mng_names = component_mng_names or set(
        med_ref.component_managers.keys()).intersection(
        med_new.component_managers.keys())
    for component_mng_name in component_mng_names:
        component_name = med_ref.component_managers[
            component_mng_name].component_name
        ref_mean, ref_risk = get_mean_risk(med_ref, component_mng_name)
        new_mean, new_risk = get_mean_risk(med_new, component_mng_name)

        # Compute the probability to find the observed moment
        # in the Gaussian distribution fitted to the moments
        # computed from the climate data
        q = 0.05
        # For the mean
        ref_mean_like = xr.zeros_like(ref_mean)

        n = new_mean.shape[0]

        # Loop over all dimensions
        for it in ref_mean_like.coords['time']:
            for k in ref_mean_like.coords[dim_comp_reg_name]:
                loc = {'time': it, dim_comp_reg_name: k}
                # Fit a normal distribution to the climate moments
                x = new_mean.loc[{dim_comp_reg_name: k}]
                s = x.std(ddof=1)
                ref_mean_like.loc[loc] = - t.ppf(
                    q/2, df=n - 1, scale=s * np.sqrt(1+1/n))

        # For the covariance
        ref_risk_like = xr.zeros_like(ref_risk)
        # Loop over all dimensions
        for it in ref_risk_like.coords['time']:
            for k in ref_risk_like.coords[dim_comp_reg_name]:
                loc = {'time': it, dim_comp_reg_name: k}
                # Fit a normal distribution to the climate moments
                x = new_risk.loc[{dim_comp_reg_name: k}]
                s = x.std(ddof=1)
                ref_risk_like.loc[loc] = -t.ppf(
                    q/2, df=n - 1, scale=s * np.sqrt(1+1/n))

        # Check which risk observations fall inside the confidence interval
        inside = ((ref_risk.mean('time') > (
            new_risk.mean('time') - ref_risk_like.mean('time'))) &
            (ref_risk.mean('time') < (
                new_risk.mean('time') + ref_risk_like.mean('time'))))

        prec = 1
        np.set_printoptions(precision=prec)
        med_ref.log.info('risk for {}'.format(component_name))
        med_ref.log.info('Observed:')
        med_ref.log.info(ref_risk.mean('time').sel(
            component_name=component_name).values * 100)
        med_ref.log.info('Computed:')
        ua = uarray((new_risk.mean('time').sel(component_name=component_name)
                     .values * 100).round(prec), (ref_risk_like.mean(
                         'time').sel(component_name=component_name).values
            * 100).round(prec))
        s = '['
        for (k, (u, ins)) in enumerate(
                zip(ua, inside.sel(component_name=component_name).values)):
            s += repr(u)
            s += ', ' if k < (len(ua) - 1) else ''
        s += ']'
        med_ref.log.info(s)


def get_mean_risk(med, component_mng_name, **kwargs):
    dim_comp_reg_name = 'component_region'
    dim_comp_reg = {dim_comp_reg_name: (
        'component', 'region_multi')}

    # Get result
    comp_ref = med.component_managers[component_mng_name]
    component_name = comp_ref.component_name
    comp_ref.get_result(**kwargs)
    res_name = med.cfg['component_managers'][component_mng_name]
    da = comp_ref.result[res_name]

    # Expand component dimension
    da = da.expand_dims('component').assign_coords(
        component=[component_name])

    # Remove NaNs
    da = da[~da.isnull().any(['region'])]

    # Stack
    da = da.stack(**dim_comp_reg)
    coord_comp_reg = da.coords[dim_comp_reg_name]
    n_comp_reg = len(coord_comp_reg)

    # Sub-sample, if needed
    if med.cfg['frequency'] == 'day':
        da = da.resample(time='D').mean('time')

    # Get mean capacity factors for each year
    gp = da.resample(time='Y')
    da_mean = gp.mean('time')

    # Get the capacity factor covariances for each year
    time = pd.to_datetime(list(gp.groups))
    coords = [('time', time), coord_comp_reg]
    da_risk = xr.DataArray(np.empty((time.shape[0], n_comp_reg)),
                           coords=coords)
    for year, group in gp:
        da_risk.loc[{'time': year}] = group.std('time')

    return da_mean, da_risk
