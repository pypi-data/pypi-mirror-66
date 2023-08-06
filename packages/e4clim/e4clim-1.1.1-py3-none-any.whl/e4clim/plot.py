"""Various plot functions."""
import os
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pandas.plotting import register_matplotlib_converters
from .geo import GEO_VARIABLE_NAME
from .container import load_config

# Register matplotlib datetime-converter
register_matplotlib_converters()

#: Default plot-colors.
COLORS = rcParams['axes.prop_cycle'].by_key()['color']


def plot_mask(data_src, crs=None, facecolor='moccasin', edgecolor='dimgrey',
              **kwargs):
    """ Plot the mask assigning climate grid points to regions.

    :param data_src: Data source.
    :param crs: Coordinate Reference System. Default is
      :py:class:`cartopy.crs.LambertAzimuthalEqualArea`.
    :param facecolor: Face color of the regions. Default is `'moccasin'`.
    :param edgecolor: Edge color of the regions. Default is `'dimgrey'`.
    :type data_src: :py:class:`.data_source.DataSourceBase`
    :type crs: :py:class:`cartopy.crs.ABCMeta`
    :type facecolor: str
    :type edgecolor: str
    """
    # Configuration
    med = data_src.med
    cfg_plot = load_config(med, 'plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    fig_dir = med.cfg.get_plot_directory(data_src, **kwargs)
    markersize = 5
    facecolor = facecolor or cfg_plot.get('region_facecolor') or 'moccasin'
    edgecolor = edgecolor or cfg_plot.get('region_edgecolor') or 'dimgrey'
    crs = crs or ccrs.LambertAzimuthalEqualArea()

    # Get mask
    data_src.get_mask(**kwargs)
    mask = data_src.mask

    # Convert geometry to CRS
    gdf = med.geo_src.get_data(variable_names=GEO_VARIABLE_NAME)[
        GEO_VARIABLE_NAME]
    gdf_crs = gdf.to_crs(crs.proj4_init)

    # Plot
    if not cfg_plot.get('no_verbose'):
        med.log.info('Plotting {} mask for {}'.format(
            med.geo_src.name, data_src.name))
    fig = plt.figure()
    ax = plt.axes(projection=crs)
    ax.set_xlabel('Longitude', fontsize=cfg_plot['fs_default'])
    ax.set_ylabel('Latitude', fontsize=cfg_plot['fs_default'])

    # Plot regions
    gdf_crs.plot(ax=ax, facecolor=facecolor, edgecolor=edgecolor)

    # Get grid points within regions
    ilat_in, ilon_in = np.where(mask['mask'] > 1)

    for ilat, ilon in zip(ilat_in, ilon_in):
        place_id = int(mask['mask'][ilat, ilon])
        if len(mask.lat.dims) > 1:
            lat, lon = mask.lat[ilat, ilon], mask.lon[ilat, ilon]
        else:
            lat, lon = mask.lat[ilat], mask.lon[ilon]
        ax.scatter(lon, lat, s=markersize,
                   transform=ccrs.Geodetic(),
                   c=COLORS[place_id % len(COLORS)])
    mask_in = mask.mask[ilat_in, ilon_in]
    ax.set_extent([mask_in.lon.min(), mask_in.lon.max(),
                   mask_in.lat.min(), mask_in.lat.max()])
    ax.set_title('{} {}'.format(med.geo_src.name, data_src.name))

    fig_filename = 'mask{}.{}'.format(data_src.get_mask_postfix(), fig_format)
    fig_filepath = os.path.join(fig_dir, fig_filename)
    if not cfg_plot.get('no_verbose'):
        med.log.info('Saving figure for {} mask for {} to {}'.format(
            med.geo_src.name, data_src.name, fig_filepath))
    fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if cfg_plot['show']:
        plt.show(block=False)


def plot_data_source(data_src, per_region=None, **kwargs):
    """ Plot data from a given source.

    :param data_src: Data source.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
      Default is `False`.
    :type data_src: :py:class:`.data_source.DataSourceBase`
    :type per_region: bool

    .. seealso:: :py:func:`plot_regional_dataset`
    """
    fig_dir = data_src.med.cfg.get_plot_directory(data_src, **kwargs)
    info_msg = ' {}'.format(data_src.name)

    # Get data
    data_src.get_data(**kwargs)

    # Plot dataset
    for variable_name in data_src.variable_names:
        plot_regional_dataset(
            data_src, variable_name, fig_dir=fig_dir, info_msg=info_msg,
            per_region=per_region, **kwargs)


def plot_result(result_mng, result_name='result',
                stage=None, per_region=None, **kwargs):
    """ Plot features of a given result manager.

    :param result_mng: Result manager of variable for which to plot
      features.
    :param result_name: `'feature'` or `'prediction'`.
    :param stage: Modeling stage: `'fit'` or `'predict'`.
      Should be provided for `'fit'`. Default is `None`.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
      Default is `False`.
    :type result_mng: :py:class:`.component.ResultManager`
    :type result_name: str
    :type stage: str

    .. seealso:: :py:func:`plot_regional_dataset`
    """
    # Get data
    info_msg = ' {}'.format(result_name)
    if result_name == 'feature':
        # Plot feature
        # Make sure that result is loaded and get data
        result_mng.extract(stage, **kwargs)
        data_src = result_mng.feature[stage]
        if not data_src.data:
            return
        info_msg += ' to {}'.format(stage)
    elif result_name == 'result':
        # Plot prediction or (extracted) output
        # Make sure that result is loaded and get data
        result_mng.get_data(**kwargs)

    info_msg += ' {}'.format(result_mng.component_mng.name)
    fig_dir = result_mng.med.cfg.get_plot_directory(
        result_mng.component_mng, **kwargs)

    for variable_name in result_mng.variable_names:
        plot_regional_dataset(
            result_mng, variable_name, fig_dir=fig_dir, info_msg=info_msg,
            per_region=per_region, **kwargs)


def plot_regional_dataset(data_src, variable_name, fig_dir='', info_msg='',
                          per_region=None, **kwargs):
    """Plot all variable of a regional dataset.

    :param data_src: Dataset.
    :param variable_name: Variable name.
    :param fig_dir: Directory in which to save figure.
    :param info_msg: Log and title information message.
    :param per_region: If `True`, plot on a separate figure for each region.
      If `None`, try reading it from mediator configuration.
      Default is `False`.
    :type data_src: mapping
    :type variable_name: str
    :type fig_dir: str
    :type info_msg: str
    :type per_region: bool
    """
    med = data_src.med
    cfg_plot = load_config(med, 'plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    per_region = per_region or cfg_plot.get('per_region', False)

    if not cfg_plot.get('no_verbose'):
        med.log.info('Plotting {} {}'.format(info_msg, variable_name))
    var = data_src.get_data()[variable_name]
    if not cfg_plot.get('no_verbose'):
        med.log.info('Variable: {}'.format(variable_name))

    # Define y label with units
    units = var.attrs.get('units')
    sunits = ' ({})'.format(units) if (units and (units != '')) else ''
    ylabel = '{}{}'.format(variable_name, sunits)

    # Plot per region
    if not hasattr(var, 'region'):
        # Check if regional data
        var = var.expand_dims(dim='region', axis=-1).assign_coords(
            region=['all'])
    time = var.indexes['time']
    freq_data = time.inferred_freq
    if freq_data is None:
        if (time[1] - time[0]).seconds == 3600:
            freq_data = 'H'
    freq_data = freq_data.upper()
    if ((med.cfg['frequency'] == 'day') and
            (freq_data in ['H', '1H'])):
        var = var.resample(time='D').mean('time')
    for ir, reg_label in enumerate(var.indexes['region']):
        plot_postfix = '_{}'.format(reg_label) if per_region else ''
        reg_msg = ' - {}'.format(reg_label) if per_region else ''
        if per_region or (ir == 0):
            fig, ax = plt.subplots(1, 1)
            da = var.loc[{'region': reg_label}]
            time = da.indexes['time']
            try:
                for component_name in var.indexes['component']:
                    label = '{} {}'.format(component_name, reg_label)
                    ax.plot(time, da.loc[{'component': component_name}],
                            label=label)
            except KeyError:
                ax.plot(time, da, label=reg_label)

        last = (ir == len(var.indexes['region']) - 1)
        if not per_region and last:
            ax.legend(loc='best')
        if per_region or last:
            # Set axes
            ax.set_xlim(time[0], time[-1])
            ax.set_xlabel('time', fontsize=cfg_plot['fs_default'])
            ax.set_ylabel(ylabel, fontsize=cfg_plot['fs_default'])
            ax.set_title('{}{} {}'.format(reg_msg, info_msg, variable_name))

            # Save figure
            result_postfix = data_src.get_data_postfix(
                variable_name=variable_name, **kwargs)
            fig_filename = '{}{}{}.{}'.format(
                variable_name, result_postfix, plot_postfix, fig_format)
            fig_filepath = os.path.join(fig_dir, fig_filename)
            if not cfg_plot.get('no_verbose'):
                med.log.info('Saving figure to {}'.format(fig_filepath))
            fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if cfg_plot['show']:
        plt.show(block=False)


def plot_generation_feature(result_mng, stage=None, **kwargs):
    """Plot generation features of a given result manager.

    :param result_mng: Result manager for which to plot features.
    :param stage: Modeling stage: `'fit'` or `'predict'`.
      Should be provided Default is `None`.
    :type result_mng: :py:class:`.component.ResultManager`
    :type stage: str
    """
    # Plot
    med = result_mng.med
    cfg_plot = load_config(med, 'plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    fig_dir = med.cfg.get_plot_directory(
        result_mng.component_mng, **kwargs)
    os.makedirs(fig_dir, exist_ok=True)

    if not cfg_plot.get('no_verbose'):
        med.log.info('Plotting features to {} {}'.format(
            stage, result_mng.name))

    # Get data
    result_mng.extract(stage)
    data_src = result_mng.feature[stage]
    if not data_src.data:
        return
    result_postfix = data_src.get_data_postfix(**kwargs)

    # Configure
    units = {'day': 'Wh/d', 'hour': 'Wh/h'}[med.cfg['frequency']]
    sample_dict = {'hour': 'H', 'day': 'D', 'week': 'W', 'month': 'M',
                   'year': 'Y'}
    sampling = sample_dict[cfg_plot['frequency']]

    # Define groups to plot
    if result_mng.component_mng.component_name == 'pv':
        groups = {
            # 'irradiance': {
            #     'Irradiance (' + units + '/m2)':
            #     ['global_horizontal_et', 'global_horizontal_surf',
            #      'glob_tilted_surf']},
            'generation': {
                'PV Generation (' + units + ')': ['generation'],
                'Cell Efficiency': ['cell_efficiency']},
            'capacity_factor': {
                'Capacity Factor': ['capacity_factor']}
        }
    elif result_mng.component_mng.component_name in [
            'wind', 'wind-onshore', 'wind-offshore']:
        groups = {
            'generation': {
                'Wind Generation (' + units + ')': ['generation']},
            'capacity_factor': {
                'Capacity Factor': ['capacity_factor']}
        }

    # Get regions
    regions = list(data_src.data.values())[0].indexes['region']

    # Plot for each region
    for reg_label in regions:
        plot_postfix = '_{}_{}'.format(reg_label, cfg_plot['frequency'])

        # Plot per groups
        for group_name, group in groups.items():
            fig = plt.figure()
            ax0 = fig.add_subplot(111)
            any_plot = False
            for k, (label, variable_names) in enumerate(group.items()):
                ax = ax0 if k == 0 else ax0.twinx()
                for iv, variable_name in enumerate(variable_names):
                    da_reg = data_src.get(variable_name)
                    if da_reg is not None:
                        da_reg = da_reg.loc[{'region': reg_label}]
                        da = da_reg.resample(time=sampling).mean(
                            'time', keep_attrs=True)
                        tm = da.indexes['time']
                        ic = (k * len(variable_names) + iv) % len(COLORS)
                        ax.plot(tm, da, label=da.attrs.get('long_name'),
                                color=COLORS[ic])
                        any_plot = True
                ax.set_ylabel(label, fontsize=cfg_plot['fs_default'],
                              color=COLORS[k])
                if len(variable_names) > 1:
                    ax.legend()
            if any_plot:
                ax0.set_xticks(ax.get_xticks()[::2])
                ax0.set_xlabel('time', fontsize=cfg_plot['fs_default'])
                ax0.set_title('{} {} {} {}'.format(
                    reg_label, result_mng.component_mng.name, stage,
                    cfg_plot['frequency']))
                fig_filename = '{}{}{}.{}'.format(
                    group_name, result_postfix, plot_postfix, fig_format)
                fig_filepath = os.path.join(fig_dir, fig_filename)
                if not cfg_plot.get('no_verbose'):
                    med.log.info('Saving figure to {}'.format(fig_filepath))
                fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if cfg_plot['show']:
        plt.show(block=False)


def plot_geo_dist(
        optimizer, lat, lon, capa_pv, capa_wind, mean_penetration=None,
        margin=2., alpha=1., n_markers=4, ms_max=1300., capa_max=10000.,
        trans=0.006, crs=None, facecolor=None, edgecolor=None,
        text=False, units='MW', text_format='{:.1f}', **kwargs):
    """ Plot geographical and technological distribution of RES capacity.

    :param optimizer: Optimizer.
    :param lat: Mean latitude of the regions.
    :param lon: Mean longitude of the regions.
    :param capa_pv: PV capacities.
    :param capa_wind: Wind capacities.
    :param cfg_plot: Plot configuration.
    :param mean_penetration: Penetration rate to add as annotation.
      Default is `None`, in which case no annotation is added.
    :param margin: Margin at the borders of the plot.
      Default is `2` points.
    :param alpha: Alpha value for the markers colors.
      Default is `1`.
    :param n_markers: Number of markers in legend.
      Default is `4`.
    :param ms_max: Maximum marker size.
      Default is `1300`.
    :param capa_max: Maximum capacity in legend.
      Default is `10000`.
    :param trans: Translation factor to seperate
      markers of the different technologies. Default is `0.006`.
    :param crs: Coordinate Reference System. Default is
      :py:class:`cartopy.crs.LambertAzimuthalEqualArea`.
    :param facecolor: Face color of the regions. Default is `'moccasin'`.
    :param edgecolor: Edge color of the regions. Default is `'dimgrey'`.
    :param text: Whether to add text boxes. Default is False.
    :param units: The units of the given data.
    :param text_format: Format of the text boxes.
    :type optimizer: :py:class:`.optimization.OptimizerBase`
    :type lat: sequence
    :type lon: sequence
    :type capa_pv: sequence
    :type capa_wind: sequence
    :type cfg_plot: dict
    :type mean_penetration: float
    :type margin: float
    :type alpha: float
    :type n_markers: int
    :type ms_max: float
    :type capa_max: float
    :type trans: float
    :type crs: :py:class:`cartopy.crs.ABCMeta`
    :type facecolor: str
    :type edgecolor: str
    :type text: bool
    :type units: str
    :type text_format: str
    """
    cfg_plot = load_config(optimizer.med, 'plot')
    facecolor = facecolor or cfg_plot.get('region_facecolor') or 'moccasin'
    edgecolor = edgecolor or cfg_plot.get('region_edgecolor') or 'dimgrey'
    crs = crs or ccrs.LambertAzimuthalEqualArea()

    # Convert geometry to CRS
    geo_src = optimizer.med.geo_src
    gdf = geo_src.get_data(variable_names=GEO_VARIABLE_NAME,
                           **kwargs)[GEO_VARIABLE_NAME]
    gdf_crs = gdf.to_crs(crs.proj4_init)

    fig = plt.figure(figsize=[12, 9])
    ax = plt.axes(projection=crs)
    ax.set_xlabel('Longitude', fontsize=cfg_plot['fs_default'])
    ax.set_ylabel('Latitude', fontsize=cfg_plot['fs_default'])

    # Plot regions
    gdf_crs.plot(ax=ax, facecolor=facecolor, edgecolor=edgecolor)

    # capa_max = np.max([capa_pv.max(), capa_wind.max()])
    leg_size = (np.round(np.linspace(0., 1., n_markers + 1)[1:], 2)
                * np.round(capa_max, -int(np.log10(capa_max)) + 1))
    exp = 1
    fact = ms_max / leg_size.max()**exp
    trans *= (lon.max() - lon.min()) / 2
    trans_lon = trans * (lon.max() - lon.min()) / 2
    trans_lat = trans * (lat.max() - lat.min()) / 2

    # Draw capacity
    s = capa_pv**exp * fact
    ax.scatter(lon - trans * np.sqrt(s), lat, s=s, c=COLORS[0],
               marker='o', alpha=alpha, transform=ccrs.Geodetic())

    s = capa_wind**exp * fact
    ax.scatter(lon + trans * np.sqrt(s), lat, s=s, c=COLORS[1],
               marker='o', alpha=alpha, transform=ccrs.Geodetic())

    # Add text
    if text:
        for k, (c_pv, c_wind) in enumerate(zip(capa_pv, capa_wind)):
            transform = ccrs.Geodetic()._as_mpl_transform(ax)
            # Annotate PV
            t_lon = lon[k] - 30 * trans_lon
            t_lat = lat[k] - 1.5 * trans_lat
            ax.annotate(text_format.format(c_pv.values), xy=(t_lon, t_lat),
                        xycoords=transform, fontsize='xx-large')
            # Annotate wind
            t_lon = lon[k] + 15 * trans_lon
            t_lat = lat[k] - 1.5 * trans_lat
            ax.annotate(text_format.format(c_wind.values), xy=(t_lon, t_lat),
                        xycoords=transform, fontsize='xx-large')

    # Draw legend
    h_pv = [plt.plot([-1e9], [-1e9], linestyle='',
                     marker='$\mathrm{PV}$', color='k', markersize=20)[0]]
    h_wind = [plt.plot([-1e9], [-1e9], linestyle='',
                       marker='$\mathrm{Wind}$', color='k', markersize=40)[0]]
    h_pv += [plt.scatter(
        [], [], s=leg_size[s]**exp * fact, c=COLORS[0],
        marker='o', alpha=alpha) for s in np.arange(n_markers)]
    h_wind += [plt.scatter([], [], s=leg_size[s]**exp * fact,
                           c=COLORS[1], marker='o',
                           alpha=alpha) for s in np.arange(n_markers)]
    l_pv, l_wind = [''], ['']
    l_pv += ['' for s in np.arange(n_markers)]
    l_wind += ['{:} MW'.format(int(leg_size[s])) for s in np.arange(n_markers)]
    l_wind += ['{:} {}'.format(int(leg_size[s]), units)
               for s in np.arange(n_markers)]
    ax.legend(h_pv + h_wind, l_pv + l_wind, loc='best', handletextpad=1.,
              labelspacing=2.5, borderpad=1.5, ncol=2, columnspacing=1.5)

    if mean_penetration is not None:
        starget = '$\mu^* = {:.1f}\%$'.format(mean_penetration * 100)
        plt.annotate(starget, xy=(0.7, 0.02), xycoords='axes fraction',
                     fontsize=cfg_plot['fs_latex'])

    # Set extent
    tb = gdf_crs.total_bounds
    extent = tb[0], tb[2], tb[1], tb[3]
    ax.set_extent(extent, crs)

    return fig


def plot_band_spectrum(med, ds, filt, time_slice=None,
                       plot_freq=['Y', 'D', 'H'], var_ylims={},
                       add_legend=False, **kwargs):
    """Plot band spectrum, i.e. the integration of power spectrum over
    frequency bands.

    :param med: Mediator.
    :param ds: Dataset of output variables of components.
    :param filt: Filtered data.
    :param time_slice: Period to select.
    :param plot_freq: Frequencies for which to plot.
      Default is `['Y', 'D', 'H']`.
    :param var_ylims: Mapping of y-axis limits to result-manager names.
    :param add_legend: Whether to add the legend. Default is `False`.
    :type med: :py:class:`.mediator.Mediator`
    :type ds: mapping
    :type filt: mapping
    :type time_slice: slice
    :type plot_freq: sequence
    :type var_ylims: mapping
    :type add_legend: bool
    """
    cfg_plot = load_config(med, 'plot')
    fig_format = cfg_plot['savefigs_kwargs']['format']
    lw = {'Y': 3, 'D': 2, 'H': 1}
    zo = {'Y': 3, 'D': 2, 'H': 1}
    labels = {'Y': 'Yearly-mean', 'D': 'Daily-mean', 'H': 'Hourly'}
    var_labels = {'demand': '', 'capacity_factor': 'Capacity Factor'}
    comp_labels = {
        'demand': 'Demand', 'pv': 'PV', 'wind': 'Wind',
        'wind-onshore': 'Onshore Wind', 'wind-offshore': 'Offshore Wind'}
    figsize = kwargs.get('figsize') or rcParams['figure.figsize']
    for component_mng_name, ds_comp in ds.items():
        component_mng = med[component_mng_name]
        fig_dir = med.cfg.get_plot_directory(component_mng, **kwargs)
        for res_variable_name, da in ds_comp.items():
            result_mng = component_mng[res_variable_name]
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
            filt_var = filt[component_mng_name][res_variable_name]
            for ifr, freq in enumerate(filt_var):
                dum = filt_var[freq]
                if time_slice is not None:
                    dum = dum.sel(time=time_slice)
                if ifr == 0:
                    ts = dum
                else:
                    ts += dum
                if freq in plot_freq:
                    ax.plot(ts.time, ts, linewidth=lw[freq], zorder=zo[freq],
                            label=labels[freq])

            ylabel = '{} {}'.format(
                comp_labels[component_mng_name], var_labels[res_variable_name])
            units = da.attrs.get('units')
            if units:
                ylabel += ' ({})'.format(units)
            elif res_variable_name == 'capacity_factor':
                ylabel += ' (%)'
            ax.set_ylabel(ylabel, fontsize=cfg_plot['fs_default'])
            # Add limits
            ylim = var_ylims.get(res_variable_name)
            if ylim is not None:
                ax.set_ylim(ylim)

            # Add legend only if regions not present
            if add_legend:
                ax.legend(loc='upper right')

            # Save figure
            result_postfix = result_mng.get_data_postfix(**kwargs)
            if time_slice is not None:
                result_postfix += '_{}_{}'.format(
                    time_slice.start, time_slice.stop)
            fig_filename = 'filtered_{}{}.{}'.format(
                result_mng.name, result_postfix, fig_format)
            fig_filepath = os.path.join(fig_dir, fig_filename)
            if not cfg_plot.get('no_verbose'):
                med.log.info('Saving figure to {}'.format(fig_filepath))
            fig.savefig(fig_filepath, **cfg_plot['savefigs_kwargs'])

    if cfg_plot['show']:
        plt.show(block=False)
