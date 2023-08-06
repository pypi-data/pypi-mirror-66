"""Modifier to weight dataset by grid area."""
import numpy as np
import xarray as xr
import iris
from ..actuator_base import ExtractorBase


class Actuator(ExtractorBase):
    """Actuator to weight a gridded dataset by grid-boxes areas."""

    def transform(self, ds=None, **kwargs):
        """Apply modifier to data source.

        :param ds: Dataset to transform.
        :type ds: :py:class:`xarray.Dataset`

        :returns: Modified dataset.
        :rtype: Same as :py:obj:`data_src.data`
        """
        for da_name, da in ds.items():
            if not self.cfg.get('no_verbose'):
                self.log.info(
                    'Area weighting {} {}'.format(
                        self.component_mng.name, da_name))

            # Get cube from array
            cube = da.to_iris()
            try:
                # Try to get area from existing bounds
                area = iris.analysis.cartography.area_weights(cube)
            except ValueError:
                # Get area from guessed bounds
                try:
                    cube.coord('longitude').guess_bounds()
                    cube.coord('latitude').guess_bounds()
                except iris.exceptions.CoordinateNotFoundError:
                    cube.coord('grid_longitude').guess_bounds()
                    cube.coord('grid_latitude').guess_bounds()
                area = iris.analysis.cartography.area_weights(cube)

            # Convert to array
            da_area = xr.DataArray(area, coords=da.coords)

            if self.cfg.get('normalize'):
                # Normalize by mean area
                da_area /= da_area.sum() / np.prod(da_area.shape)

            # Weight by area
            ds[da_name] *= da_area

        return ds

    def get_extractor_postfix(self, **kwargs):
        """Get extractor postfix.

        returns: Postfix.
        rtype: str
        """
        postfix = '{}_weighted'.format(
            super(Actuator, self).get_extractor_postfix(**kwargs))

        postfix += '_norm' * self.cfg['normalize']

        return postfix
