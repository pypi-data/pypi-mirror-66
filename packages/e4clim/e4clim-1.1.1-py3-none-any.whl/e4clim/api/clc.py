"""Copernicus Land Cover API."""
import os
import numpy as np
import pandas as pd
import xarray as xr
from fiona.crs import from_epsg
import rasterio
from shapely.geometry import Point
import geopandas as gpd
from pkg_resources import resource_stream
from ..geo import get_mask_path
from ..data_source import DataSourceLoaderBase


class DataSource(DataSourceLoaderBase):
    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Naming constructor.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        name = name or 'clc'
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def download(self, *args, **kwargs):
        """Warn that :py:meth:`download` method not implemented."""
        self.log.warning(
            '{} data download not implemented'.format(self.name))

    def load(self, *args, **kwargs):
        # Get configuration file to use and import it
        data_dir = self.cfg['dir'] if 'dir' in self.cfg \
            else self.med.cfg['data_dir']
        crs_wgs84 = from_epsg(4326)

        # Read the mask
        mask_filepath = get_mask_path(self.cfg, self.name)
        ds_mask = xr.load_dataset(mask_filepath)

        # Get regular grid limits
        lat, lon = ds_mask.lat.values, ds_mask.lon.values
        if len(ds_mask.lat.shape) > 1:
            n_lat, n_lon = ds_mask.lat.shape
        else:
            n_lat, n_lon = len(ds_mask.lat), len(ds_mask.lon)
            lat, lon = np.tile(lat, (n_lon, 1)).T, np.tile(lon, (n_lat, 1))
        dlat, dlon = np.empty((n_lat + 1, n_lon)), np.empty((n_lat, n_lon + 1))
        dlat[1:-1] = (lat[1:] - lat[:-1]) / 2
        dlat[0] = dlat[1]
        dlat[-1] = dlat[-2]
        dlon[:, 1:-1] = (lon[:, 1:] - lon[:, :-1]) / 2
        dlon[:, 0] = dlon[:, 1]
        dlon[:, -1] = dlon[:, -2]
        lat_lim = np.empty((n_lat + 1, n_lon))
        lat_lim[:-1] = lat - dlat[:-1]
        lat_lim[-1] = lat[-1] + dlat[-1]
        lon_lim = np.empty((n_lat, n_lon + 1))
        lon_lim[:, :-1] = lon - dlon[:, :-1]
        lon_lim[:, -1] = lon[:, -1] + dlon[:, -1]
        # Back to 1D (other grids not yet implemented)
        lat_lim, lon_lim = lat_lim[:, 0], lon_lim[0]

        # Read land cover - roughness length map (CLC/Global Wind Atlas)
        resource_name = '../data/' + 'landuse_roughness_GWA1.csv'
        with resource_stream(__name__, resource_name) as f:
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Reading land use to roughness map from {}'.format(
                        resource_name))
            df_map = pd.read_csv(f, index_col=0, header=0).loc[
                :, 'Roughness_Length']
        d_map = df_map.dropna().to_dict()

        # Read the raster file
        filename = 'g' + self.cfg['resolution'] + '_' + 'clc' \
            + self.cfg['year'][2:] + '_V' + self.cfg['version'] \
            + '.' + self.cfg['fileFormat']
        filepath = os.path.join(data_dir, filename)
        if not self.cfg.get('no_verbose'):
            self.log.info('Reading land cover from {}'.format(filepath))
        ds_land = rasterio.open(filepath, 'r')

        # Get window
        lat0, lon0 = lat.min(), lon.min()
        pt0 = gpd.GeoSeries(Point(lon0, lat0),
                            crs=crs_wgs84).to_crs(ds_land.crs)
        latf, lonf = lat.max(), lon.max()
        ptf = gpd.GeoSeries(Point(lonf, latf),
                            crs=crs_wgs84).to_crs(ds_land.crs)
        xmin, ymin, xmax, ymax = float(pt0.x), float(
            pt0.y), float(ptf.x), float(ptf.y)
        window = ds_land.window(xmin, ymin, xmax, ymax)
        window = window.round_offsets().round_lengths()

        # Values
        values = ds_land.read(window=window)[0]

        jleft, itop, jright, ibot = window.flatten()
        jright += jleft
        ibot += itop
        count = xr.zeros_like(ds_mask.mask)
        roughness = xr.zeros_like(ds_mask.mask).astype(float)
        roughness.name = 'roughness_length'
        si, sj = self.cfg['sampling'], self.cfg['sampling']
        if not self.cfg.get('no_verbose'):
            self.log.info(
                'Averaging the land cover over the {} grid'.format(self.name))
        for i in range(itop, ibot, si):
            for j in range(jleft, jright, sj):
                # Get the roughness length and continue only if
                # it has a meaning
                rl = d_map.get(values[i - itop, j - jleft])
                if rl is not None:
                    # Get the longitude and latitude of this point
                    xy = ds_land.xy(i, j)
                    pt = gpd.GeoSeries(
                        Point(*xy), crs=ds_land.crs).to_crs(crs_wgs84)
                    lon_pt, lat_pt = pt[0].coords[0]
                    # Find grid box of the mask to which the land cover point
                    # belongs
                    ilat_mask = np.searchsorted(
                        lat_lim, lat_pt, side='right') - 1
                    if (ilat_mask >= 0) & (ilat_mask < n_lat):
                        jlon_mask = np.searchsorted(
                            lon_lim, lon_pt, side='right') - 1
                        if (jlon_mask >= 0) & (jlon_mask < n_lon):
                            roughness[ilat_mask, jlon_mask] += rl
                            count[ilat_mask, jlon_mask] += 1
        roughness /= count

        # Save the dataset
        postfix = '_{}{}_{}'.format(
            'clc', str(self.cfg['year']), self.name)
        filename = 'roughness_length' + postfix + '.nc'
        filepath = os.path.join(self.med.cfg['data_dir'], 'climate', filename)
        if not self.cfg.get('no_verbose'):
            self.log.info('Saving roughness length to '.format(filepath))
        roughness.to_netcdf(filepath)

        ds_land.close()
        ds_mask.close()
