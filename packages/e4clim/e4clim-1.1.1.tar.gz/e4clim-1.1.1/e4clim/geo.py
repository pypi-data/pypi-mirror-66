"""Geographic-data and mask base definitions."""
import os
from collections import OrderedDict
from abc import ABC, abstractmethod
from pkg_resources import resource_stream
import requests
import zipfile
from io import BytesIO
from shapely.geometry import Point
from fiona.crs import from_epsg
import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
import oyaml as yaml
import difflib
from .data_source import DataSourceBase, DataSourceLoaderBase, MultiDataSource
from .container import ensure_collection

#: Geographic-variable name.
GEO_VARIABLE_NAME = 'border'


class GeoDataSourceBase(DataSourceBase):
    """Geographic data-source abstract base class."""

    def __init__(self, med, name, cfg=None, variable_names=None, **kwargs):
        """Convenience constructor for default geographic data source."""
        variable_names = variable_names or [GEO_VARIABLE_NAME]
        super(GeoDataSourceBase, self).__init__(
            med, name, cfg=cfg, variable_names=variable_names,
            data_as_dict=True, **kwargs)

        #: Area and zones/regions description per data sources.
        self.area_places_sources = None

        #: Area-zones/regions mapping for data source.
        self.area_places = None

        #: Area-regions mapping for data source.
        self.area_regions = None

        #: Place-area mapping.
        self.place_area = None

        #: Areas.
        self.areas = None

        #: Region-zone/region mapping.
        self.region_place = None

        #: Zone/region-region mapping.
        self.place_regions = None

        #: Data-source region names.
        self.region_names = None

        #: Zone/region names.
        self.place_names = None

        #: Zone/region indices = None
        self.place_indices = None

        # Get mappings and list
        self._init_regions_places(**kwargs)

        #: Child column.
        if hasattr(self, 'cfg') and getattr(self, 'cfg'):
            self._child_column = self.cfg.get('child_column')

    def get_place_regions_for_source(self, src_name, area=None, **kwargs):
        """Get zone/region-regions and region-zone/region mappings
        for data source and area.

        :param src_name: Data-source name for which to get place names.
        :param area: Area for which to get place names. Default is `None`,
          in which case places for all areas are returned.
        :type src_name: str
        :type area: str

        :returns: zone/region-regions and region-zone/region mappings.
        :rtype:

          * :py:class:`dict` of :py:class:`str` to :py:class:`set`
          * :py:class:`dict` of :py:class:`str` to :py:class:`str`

        """
        # Get place names for given area but all data sources
        area_place_names = (self.area_places[area] if area is not None else
                            self.place_names)
        area_place_names = ensure_collection(area_place_names, set)
        areas = [area] if area is not None else self.areas

        # Get place-regions mapping for given area and data source
        src_area_place_regions = OrderedDict()
        for area in areas:
            src_area_place_regions.update(
                {place_name: ensure_collection(src_regions[src_name])
                 for place_name, src_regions
                 in self.area_places_sources[area].items()
                 if src_name in src_regions})

        # Get region-place mapping
        src_area_region_place = OrderedDict()
        for place_name, region_names in src_area_place_regions.items():
            src_area_region_place.update({
                region_name: place_name for region_name in region_names})

        return src_area_place_regions, src_area_region_place

    def get_total_bounds(self, epsg=4326, **kwargs):
        """Get array of min and max coordinates on each axis.

        :param epsg: EPSG code specifying output projection.
        :type epsg: int

        :returns: Array with min x, min y, max x, max y.
        :rtype: :py:class:`numpy.array`
        """
        # Get geo data
        geo_data = self.med.geo_src.get_data(
            variable_names=GEO_VARIABLE_NAME, **kwargs)[GEO_VARIABLE_NAME]

        # Transform to right CRS
        data = geo_data.to_crs(epsg=epsg) if epsg else geo_data

        # Return total bounds
        return data.total_bounds

    def read_place_coordinates(self, **kwargs):
        """Read centroid coordinates of zones/regions.

        :returns: Centroid coordinates of places.
        :rtype: :py:class:`pandas.GeoDataFrame`
        """
        # Set filepath
        file_dir = self.med.cfg.get_project_data_directory(self, **kwargs)
        filename = 'latlon{}.csv'.format(
            self.get_data_postfix(with_src_name=True, **kwargs))
        filepath = os.path.join(file_dir, filename)

        # Open and read coordinates from file
        with open(filepath, 'r') as f:
            df_coord_places = pd.read_csv(f, index_col=0)

        return df_coord_places

    def write_place_coordinates(self, **kwargs):
        """Write centroid coordinates of zones/regions."""
        # Get coordinates as data frame
        gdf = self.get(GEO_VARIABLE_NAME)
        df_coord = pd.DataFrame(index=gdf.index, columns=['lat', 'lon'])

        for place in gdf.index:
            # Get place centroid in source coordinates
            pt0 = gdf.loc[place].geometry.centroid

            # Convert to reference CRS
            pt = gpd.GeoSeries(pt0, crs=gdf.crs).to_crs(
                from_epsg(4326)).values[0]
            df_coord.loc[place] = [pt.y, pt.x]

        # Set filepath
        file_dir = self.med.cfg.get_project_data_directory(self, **kwargs)
        filename = 'latlon{}.csv'.format(
            self.get_data_postfix(with_src_name=True, **kwargs))
        filepath = os.path.join(file_dir, filename)

        # Write coordinates to file
        df_coord.to_csv(filepath)

    def _init_regions_places(self, **kwargs):
        """Set region-to-zone/region mapping :py:attr:`region_place`,
        zone/region-names list :py:attr:`place_names` and
        zone/region-to-regions mapping :py:attr:`place_regions`.

        .. note:: :py:attr:`areas` are to areas in
          `component_managers_per_area` of mediator configuration, if defined,
          or to all areas in :py:attr:`area_places_sources`.

        .. seealso:: :py:meth:`_get_area_places_sources`.
        """
        # Get area and zones/regions description per data sources
        self.area_places_sources = self._get_area_places_sources(**kwargs)

        # Get all areas from components or all described areas
        areas = set(self.med.cfg.get('component_managers_per_area') or
                    self.area_places_sources)

        # Loop over areas to define places and regions
        self.area_places = OrderedDict()
        self.area_regions = OrderedDict()
        self.region_place = OrderedDict()
        self.place_regions = OrderedDict()
        self.place_names = set()
        self.areas = set()
        for area in areas:
            # Loop over place-source names pairs
            place_sources = self.area_places_sources[area]
            for place_name, src_regions in place_sources.items():
                # Try to get region names for this data source
                if self.name in src_regions:
                    # Add area
                    self.areas.add(area)

                    # Add place to place names
                    self.place_names.add(place_name)

                    # Add place to area
                    self.area_places.setdefault(area, set()).add(place_name)

                    # Get place region-names.
                    region_names = ensure_collection(
                        src_regions[self.name], set)

                    # Add regions to area
                    self.area_regions.setdefault(area, set()).update(
                        region_names)

                    # Add place-regions pair
                    self.place_regions[place_name] = ensure_collection(
                        region_names)

                    # Add region-place pair
                    self.region_place.update(
                        {region_name: place_name
                         for region_name in region_names})

        # Get place-area mapping
        self.place_area = OrderedDict()
        for area, place_names in self.area_places.items():
            self.place_area.update(
                {place_name: area for place_name in place_names})

        # Get data-source region names
        self.region_names = set(self.region_place)

        # Get place indices
        self.place_indices = self._get_place_indices(**kwargs)

    def _get_area_places_sources(self, **kwargs):
        """Get zones/regions from file given by `places_filepath` entry of
        geo configuration.

        :returns: Places.
        :rtype: list
        """
        area_places_sources_filepath = self.med.geo_cfg.get('places_filepath')
        area_places_sources_filepath = os.path.join(*ensure_collection(
            area_places_sources_filepath))
        with open(area_places_sources_filepath, 'r') as f:
            area_places_sources = yaml.load(f, Loader=yaml.FullLoader)

        return area_places_sources

    def _get_place_indices(self, **kwargs):
        """Get place indices in mask."""
        # Create dictionary of places (independent of data grid)
        place_ids = list(range(2, len(self.place_names) + 2))
        place_indices = dict(zip(self.place_names, place_ids))

        return place_indices


class MultiGeoDataSource(MultiDataSource, GeoDataSourceBase):
    """Multiple geographic data source.
    Redefines :py:meth:`get` method to merge (geographic) variable
    in all single data sources into a single
    :py:class:`pandas.GeoDataFrame`."""

    def __init__(self, med, data_sources, task_names=set(),
                 default_tasks_value=True, **kwargs):
        """Build with :py:class:`.data_source.MultiDataSource` constructor.

        :param med: Mediator.
        :param data_sources: Data sources dictionary.
        :param task_names: Names of potential tasks for container to perform.
          Default is `set()`.
        :param default_tasks_value: If `True`, ask to perform all tasks.
          Otherwise, none. Default is `True`.
        :type med: :py:class:`.mediator.Mediator`
        :type data_sources: :py:class:`dict` of :py:class:`DataSourceBase`
        :type task_names: set
        :type default_tasks_value: bool
        """
        # Initialize as data source
        super(MultiGeoDataSource, self).__init__(
            med, data_sources, task_names=set(),
            default_tasks_value=True, **kwargs)

        # Initialize regions and places merging from single data sources
        self._init_regions_places(**kwargs)

    def _init_regions_places(self, **kwargs):
        """Set region-to-zone/region mapping :py:attr:`region_place`,
        zone/region-names set :py:attr:`place_names` and
        zone/region-to-regions mapping :py:attr:`place_regions`
        merging from single data sources.
        """
        # Make sure that the initialization is called after
        # the parents constructors are called
        if hasattr(self, 'data_sources') and getattr(self, 'data_sources'):
            # Get zones/regions description from any single data source
            self.area_places_sources = self.data_sources[
                list(self.data_sources)[0]].area_places_sources

            # Merge attributes
            self.region_place = OrderedDict()
            self.place_regions = OrderedDict()
            self.place_indices = OrderedDict()
            self.area_places = OrderedDict()
            self.place_area = OrderedDict()
            self.place_names = set()
            self.region_names = set()
            self.areas = set()
            for data_src in self.data_sources.values():
                # Merge mappings
                self.region_place.update(data_src.region_place)
                self.place_regions.update(data_src.place_regions)
                self.place_indices.update(data_src.place_indices)
                self.place_area.update(data_src.place_area)
                # Allow for multiple data sources per area
                for area, places in data_src.area_places.items():
                    self.area_places.setdefault(area, set()).update(places)

                # Merge sets
                self.place_names.update(data_src.place_names)
                self.region_names.update(data_src.region_names)
                self.areas.update(data_src.areas)

    def get(self, variable_name, default=None):
        """Get variable from data source containing variable.

        :param variable_name: Variable name.
        :param default: Default geographic data frame. Default is `None`.
        :type variable_name: str
        :type default: :py:class:`pandas.GeoDataFrame`

        :returns: Merged geographic data frame.
        :rtype: py:class:`pandas.GeoDataFrame`
        """
        return self.data.get(variable_name, default)

    def get_data(self, **kwargs):
        """Load geographic data from multiple geographic data sources
        and merge the geographic data into one geographic data frame.


        :returns: Dataset :py:attr:`data`.
        :rtype: mapping of :py:class:`str` to :py:class:`pandas.GeoDataFrame`
        """
        gdf = None

        # Get reference CRS
        data_sources = self.data_sources.copy()
        crs_as = self.med.geo_cfg.get('crs_as')
        if crs_as:
            data_src = data_sources.pop(crs_as)
            gdf = data_src.get_data(**kwargs)[GEO_VARIABLE_NAME]
            crs = gdf.crs

        for data_src in data_sources.values():
            # Get data for geo variable of single source
            gdf_single = data_src.get_data(**kwargs)[GEO_VARIABLE_NAME]

            if crs_as:
                # Convert to reference CRS
                gdf_single = gdf_single.to_crs(crs)

            # Merge geographic data frame
            gdf = gdf_single if gdf is None else pd.concat([gdf, gdf_single])

        # Assign
        self.data = {GEO_VARIABLE_NAME: gdf}

        return self.data


class DefaultMaskAPI(DataSourceLoaderBase):
    """Mask downloading mixin. To be mixed with
    :py:class:`GeoDataSourceBase`.
    """
    #: Flag allowing several downloads per area.
    ONE_DOWNLOAD_PER_AREA = False

    def download(self, **kwargs):
        """Download geographic data defining geometries of areas/zones/regions.

        :returns: Names of downloaded variables.
        :rtype: :py:class:`set` of :py:class:`str`

        .. warning:: Requires :py:meth:`get_url` and :py:meth:`get_filename`
          methods to be implemented.
        """
        src_dir = self.med.cfg.get_external_data_directory(self, **kwargs)
        previous_urls = []
        for area in self.areas:
            # Get URL and filename for area
            url = self.get_url(area=area, **kwargs)
            filename = self.get_filename(area=area, **kwargs)

            # Prevent downloading non-area specific data multiple times
            if url not in previous_urls:
                # Download geographic data for area
                self.log.info(
                    'Downloading {} geographic data for {} from {}'.format(
                        self.name, area, url))
                download_from_url(url, filename, src_dir)

                if self.ONE_DOWNLOAD_PER_AREA:
                    # Prevent future downloads
                    previous_urls.append(url)

        return {GEO_VARIABLE_NAME}

    def read_file(self, area, **kwargs):
        """Read downloaded geographical data for area.

        :param area: Geographical area for which to read the data.
        :type area: str

        :returns: Geographic data frame.
        :rtype: :py:class:`geopandas.GeoDataFrame`
        """
        src_dir = self.med.cfg.get_external_data_directory(
            self, makedirs=False, **kwargs)

        # Get directory for area
        filename = self.get_filename(area=area, **kwargs)
        filepath = os.path.join(src_dir, filename)

        # Read geographical file for area
        read_file_kwargs = self.cfg.get('read_file_kwargs') or {}
        gdf_area = gpd.read_file(filepath, **read_file_kwargs)

        return gdf_area

    def load(self, **kwargs):
        """Load geographical data for all areas.

        :returns: Geographical array with geometries.
        :rtype: mapping to :py:class:`geopandas.GeoDataFrame`

        .. note:: The geographic data is aggregated by zone.
          A zone could be the region itself,
          in which case no aggregation is performed.

        """
        gdf = None
        for area in self.areas:
            # Read file
            gdf_area = self.read_file(area, **kwargs)

            # Handle parent/child columns
            if 'parent_column' in self.cfg:
                # Get country code
                country_code = get_country_code(area, code='alpha-2')

                # Select country
                gdf_area_sel = gdf_area[gdf_area.loc[
                    :, self.cfg['parent_column']] == country_code]

                # GB/UK exception
                if (country_code == 'GB') and (len(gdf_area_sel) == 0):
                    gdf_area_sel = gdf_area[gdf_area.loc[
                        :, self.cfg['parent_column']] == 'UK']

                gdf_area = gdf_area_sel

            # Index by child-column
            gdf_area = gdf_area.set_index(self._child_column)[['geometry']]

            region_names = self.area_regions[area]
            if (len(region_names) == 1) and (area in region_names):
                # Manage country case
                gdf_area.loc[:, 'zone'] = area
                gdf_area = gdf_area.dissolve(by='zone')
            else:
                # Select requested regions for area
                gdf_area = gdf_area.loc[region_names]

                # Aggregate by zone taking places from region-place mapping
                # to preserve order.
                gdf_area.loc[:, 'zone'] = [self.region_place[region_name]
                                           for region_name in gdf_area.index]
                gdf_area = gdf_area.dissolve(by='zone')

            # Merge area
            gdf = gdf_area if gdf is None else pd.concat([gdf, gdf_area])

        # Add variable data to data source
        self.update({GEO_VARIABLE_NAME: gdf})

        # Write coordinates of places' centroids
        self.write_place_coordinates(**kwargs)

        return {GEO_VARIABLE_NAME: gdf}

    def read(self, **kwargs):
        """Read source dataset as :py:class:`geopandas.GeoDataFrame`
        from file.
        """
        filepath = self.get_data_path(
            variable_name=GEO_VARIABLE_NAME, makedirs=False, is_timeseries=False,
            **kwargs)
        if not self.cfg.get('no_verbose'):
            self.log.info('Reading {} for {} from {}'.format(
                GEO_VARIABLE_NAME, self.name, filepath))
        self[GEO_VARIABLE_NAME] = gpd.read_file(filepath).set_index('zone')

    def write(self, **kwargs):
        """Write source :py:class:`geopandas.GeoDataFrame` dataset to file.
        """
        filepath = self.get_data_path(
            variable_name=GEO_VARIABLE_NAME, is_timeseries=False, **kwargs)
        if not self.cfg.get('no_verbose'):
            self.log.info('Writing {} for {} to {}'.format(
                GEO_VARIABLE_NAME, self.name, filepath))
        self.get(GEO_VARIABLE_NAME).reset_index().to_file(filepath)


class MaskMakerBase(ABC):
    """Base mask maker. To be mixed with :py:class:`GeoDataSourceBase`.
    ..warning:: Requires :py:meth:`make_mask` method to be implemented.
    """
    @abstractmethod
    def make_mask(self, *args, **kwargs):
        """Make mask for a gridded data source."""
        raise NotImplementedError


class DefaultMaskMaker(GeoDataSourceBase, MaskMakerBase):
    """Default mask maker."""

    def make_mask(self, data_src, **kwargs):
        """Make mask for a given gridded data source, store the
        regions' geometries to :py:attr:`data` member.

        :param data_src: Gridded data source.
        :type data_src: :py:class:`.grid.GriddedDataSourceBase`

        :returns: Mask dataset.
        :rtype: :py:class:`xarrray.Dataset`
        """
        # Get regions' geometries
        self.get_data(variable_names=GEO_VARIABLE_NAME, **kwargs)

        # Download data to read the grid
        data_src.manage_download(**kwargs)

        # Get data coordinates
        coords = data_src.get_grid(**kwargs)

        # Get point region membership
        self.log.info('Assigning points to regions')
        ds_mask = get_point_region_membership(
            self.cfg, self.get(GEO_VARIABLE_NAME), self.place_indices, coords)

        # Add geographic data-source name
        ds_mask.attrs['data_source'] = self.name

        return ds_mask


def get_point_region_membership(cfg_src, gdf, place_indices, coords):
    """Assign grid-points of dataset to electricity places.

    :param cfg_src: Data source configuration.
    :param gdf: Regions' geometries.
    :param place_indices: Dictionary assigning each plae name to a place ID.
      IDs of places of interest should be larger or equal to 2.
    :param coords: Input data coordinates assigned to telectricity places.
    :type cfg_src: dict
    :type gdf: :py:class:`geopandas.GeoDataFrame`
    :type place_indices: dict
    :type coords: :py:class:`tuple` of pairs of :py:class:`str`
      and :py:class:`numpy.array`

    :returns: Dataset containing mask assigning each grid-point to a place.
    :rtype: :py:class:`xarray.Dataset`
    """
    # Get dims and coords for regular and irregular grids
    try:
        dim_names = coords.dims
        dims = tuple(coords[dim].shape[0] for dim in dim_names)
    except AttributeError:
        dim_names = coords.keys()
        dims = tuple(len(v) for v in coords.values())

    # Create an empty mask
    ds = xr.Dataset()
    ds['mask'] = xr.DataArray(np.zeros(dims, dtype=int),
                              dims=dim_names, coords=coords)

    # Add region indices
    coords = ('region', list(place_indices.keys()))
    ds['region_index'] = xr.DataArray(
        list(place_indices.values()), coords=[coords])

    # Assign points to regions
    for iy in range(ds['mask'].shape[0]):
        for ix in range(ds['mask'].shape[1]):
            # Select point and convert to regions' CRS
            try:
                lat = float(ds.lat[iy, ix].values)
                lon = float(ds.lon[iy, ix].values)
            except IndexError:
                lat = float(ds.lat[iy].values)
                lon = float(ds.lon[ix].values)
            pt = gpd.GeoSeries(
                Point(lon, lat), crs=from_epsg(4326)).to_crs(gdf.crs)

            # Select place to which this point belongs to, if any
            within = gdf.contains(pt[0])
            if within.any():
                # Get place name
                zone = gdf[within].index[0]

                # Get corresponding zone and save zone ID in mask
                # If region in no zone, set to 1
                ds['mask'][iy, ix] = place_indices[zone] if zone else 1

    # Remove empty regions
    idx_filled = np.in1d(ds.region_index, np.unique(ds.mask))
    ds = ds.loc[{'region': idx_filled}]

    return ds


def download_from_url(url, filename, src_dir):
    """Download geographic data defining borders for areas/zones/regions
    and return geometries.

    :param url: URL from which to download data.
    :param filename: Downloaded-file name.
    :param src_dir: Data destination directory.
    :type url: str
    :type filename: str
    :type src_dir: str

    .. note:: This function is not directly called from this module,
      but from API's included in this package(e.g. GISCO).
    """
    # Download data for region
    filepath = os.path.join(src_dir, filename)
    r = requests.get(url)
    if r.status_code != 200:
        raise FileNotFoundError(url)

    # Extract, if needed, or write file
    if url[-4:] == '.zip':
        zip_ref = zipfile.ZipFile(BytesIO(r.content))
        zip_ref.extractall(src_dir)
        zip_ref.close()
    else:
        with open(filepath, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def get_country_code(area, code='alpha-2'):
    """Get country code.

    :param area: Country name.
    :param code: Code name.
    :type area: str
    :type code: str

    :returns: Country code.
    :rtype: str
    """
    # Read country codes
    resource_name = 'data/iso_country_codes.csv'
    with resource_stream(__name__, resource_name) as stream:
        cc_data = pd.read_csv(stream, index_col=0)
    area_name = difflib.get_close_matches(
        area, cc_data.index.tolist(), n=1)[0]

    return cc_data.loc[area_name, code]
