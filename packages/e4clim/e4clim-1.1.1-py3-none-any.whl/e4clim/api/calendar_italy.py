"""Italian calendar."""
from collections import OrderedDict
import numpy as np
import xarray as xr
from ..data_source import DataSourceLoaderBase

#: Default data-source name;
DEFAULT_SRC_NAME = 'calendar'

#: Default variable name.
VARIABLE_NAME = 'calendar'


class DataSource(DataSourceLoaderBase):
    """Calendar for Italy."""

    def __init__(self, med, name=None, cfg=None, **kwargs):
        """Initialize Italian calendar as data_source.

        :param med: Mediator.
        :param name: Data source name.
        :param cfg: Data-source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: mapping
        """
        name = name or DEFAULT_SRC_NAME
        super(DataSource, self).__init__(med, name, cfg=cfg, **kwargs)

    def download(self, *args, **kwargs):
        """Convenience function to warn that not calendar data needs to be
        downloaded.

        :returns: Names of downloaded variable.
        :rtype: :py:class:`set` of :py:class:`str`
        """
        self.log.warning(
            '{} data need not be downloaded'.format(self.name))

        return {VARIABLE_NAME}

    def load(self, dl, **kwargs):
        """Get array of working days, holidays and saturdays for Italy,
        and store it to member :py:attr::`data`.

        :param dl: List of dates
        :type dl: pd.DatetimeIndex, datetime.datetime

        :returns: Calendar dataset.
        :rtype: :py:class:`xarray.Dataset`
        """
        # Create day type coordinate
        daytype_name_idx = OrderedDict({'work': 0, 'sat': 1, 'off': 2})
        daytype_coord = ('daytype_index', list(daytype_name_idx.values()))

        # Create array
        da = xr.DataArray(np.empty((dl.shape[0],), dtype=int),
                          coords=[('time', dl)])

        # Sundays
        off = (dl.dayofweek == 6)
        # Public holidays + Winter and Summer holidays
        # 1st of January: new year day
        a = (dl.dayofyear == 1)
        # 25th of April: liberation day
        b = ((dl.month == 4) & (dl.day == 25))
        # 1st of May: May Day
        c = ((dl.month == 5) & (dl.day == 1))
        # 8th to 21st of August: summer holidays
        d = ((dl.month == 8) & (dl.day > 6)
             & (dl.day < 22))
        # 1st of November: all saints
        e = ((dl.month == 11) & (dl.day == 1))
        # 8th of December: Feast of the Immaculate Conception
        f = ((dl.month == 12) & (dl.day == 8))
        # 25th to 31st of December: Christmas holidays
        g = ((dl.month == 12) & (dl.day >= 25))

        # Concatenate off days
        off = (off | a | b | c | d | e | f | g)
        da[off] = daytype_name_idx['off']

        # Saturdays
        sat = (dl.dayofweek == 5) & ~off
        da[sat] = daytype_name_idx['sat']

        # Working Days
        da[~sat & ~off] = daytype_name_idx['work']

        # Create dataset with daytype coordinate
        ds = xr.Dataset({VARIABLE_NAME: da})
        ds = ds.assign_coords(daytype=xr.DataArray(
            list(daytype_name_idx.keys()), coords=[daytype_coord]))

        return ds
