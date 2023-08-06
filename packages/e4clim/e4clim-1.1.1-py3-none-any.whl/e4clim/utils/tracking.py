"""Angle computations for solar applications."""
import numpy as np
import xarray as xr
import xarray.ufuncs as xrf


class SolarTracker(object):
    """Solar tracking computer. Computes the tracking surface-tilt,
    surface-azimuth and angle-of-incidence cosine. When getting an attribute,
    the variable corresponding to it is automatically computed.
    New computations are only performed if the needed attribute value is
    `None`, i.e. if it has not previously been computed.
    To perform new computations, start from a new object,
    or call :py:meth:`clear`."""

    def __init__(self, solar_computer, tilt=None, azimuth=None,
                 tracking='none', angles_in_degrees=False, **kwargs):
        """Initialize solar tracking computer.

        :param solar_computer: Solar angles computer.
        :param tilt: Surface tilt. For a tilt equal to the latitude,
          set to `'lat'`. Should be provided if :py:obj:`tracking` is
          `'vertical'` or `'none'`. Default is `None`.
        :param azimuth: Surface azimuth.
          Should be provided if :py:obj:`tracking` is `'none'`.
          Default is `None`.
        :param tracking: For east-west axis, north-south
          axis, vertical axis, or two axes, respectively set to `'ew_track'`,
          `'ns_track'`, `'vertical'`, or `'two'`. Default is `none`.
        :param angles_in_degrees: Whether angles are given in degrees instead
          of radians.
        :type solar_computer: :py:class:`.solar_calendar.SolarCalendarComputer`
        :type tilt: (sequence of) :py:class:`float`, :py:class:`str`
        :type azimuth: (sequence of) :py:class:`float`, :py:class:`str`
        :type tracking: str
        :type angles_in_degrees: bool
        """
        # Solar computer
        self.sc = solar_computer

        # Clear variables
        self._surface_tilt = None
        self._surface_azimuth = None
        self._cos_aoi = None

        # Manage tracking strategy
        self.tracking = tracking
        fact = np.deg2rad(1.) if angles_in_degrees else 1.
        if tilt == 'lat':
            self._surface_tilt = self.sc.lat
        if tracking == 'vertical':
            if self._surface_tilt is None:
                # In case not previously set by 'lat' case
                self._surface_tilt = tilt * fact
        elif 'none':
            if self._surface_tilt is None:
                # In case not previously set by 'lat' case
                self._surface_tilt = tilt * fact
            self._surface_azimuth = azimuth * fact

    @property
    def surface_tilt(self):
        """Get surface tilt.
        Computation only performed if requested attribute is `None`.
        """
        if self._surface_tilt is None:
            self._surface_tilt = getattr(
                self, self.tracking + '_track_tilt')()

        return self._surface_tilt / self.sc.fact

    @property
    def surface_azimuth(self):
        """Get surface azimuth.
        Computation only performed if requested attribute is `None`.
        """
        if self._surface_azimuth is None:
            self._surface_azimuth = getattr(
                self, self.tracking + '_track_azimuth')()

        return self._surface_azimuth / self.sc.fact

    @property
    def cos_aoi(self):
        """Get angle-of-incidence cosine.
        Computation only performed if requested attribute is `None`.
        """
        if self._cos_aoi is None:
            self._cos_aoi = getattr(
                self, self.tracking + '_track_cos_aoi')()

        return self._cos_aoi

    def ns_track_cos_aoi(self):
        """Get angle-of-incidence cosine for north-south tracking."""
        return xrf.sqrt(1. - xrf.cos(self.sc.declination)**2
                        * xrf.sin(self.sc.hour_angle)**2)

    def ew_track_cos_aoi(self):
        """Get angle-of-incidence cosine for east-west tracking."""
        return xrf.sqrt(
            xrf.cos(self.sc.zenith)**2
            + xrf.cos(self.sc.declination)**2 * xrf.sin(self.sc.hour_angle)**2)

    def vertical_track_cos_aoi(self):
        """Get angle-of-incidence cosine for east-west tracking."""
        return xrf.sqrt(
            xrf.cos(self.sc.zenith) * xrf.cos(self._surface_tilt)
            + xrf.sin(self.sc.zenith) * xrf.sin(self._surface_tilt))

    def two_track_cos_aoi(self):
        """Get angle-of-incidence cosine for east-west tracking."""
        return xr.ones_like(self.sc.zenith)

    def none_track_cos_aoi(self):
        """Get cosine of Angle of Incidence (AOI) of direct beams
        on an array."""
        return (
            xrf.sin(self.sc.zenith) * xrf.sin(self._surface_tilt)
            * xrf.cos(self._surface_azimuth - self.sc.azimuth)
            + xrf.cos(self.sc.zenith) * xrf.cos(self._surface_tilt))

    def ns_track_tilt(self):
        """Get horizontal north-south tracking/east-west axis tilt.

        :returns: Surface tilt.
        :rtype: (sequence of) :py:class:`float`
        """
        return xrf.atan(
            xrf.tan(self.sc.zenith) * xrf.fabs(xrf.cos(self.sc.azimuth)))

    def ns_track_azimuth(self):
        """Get horizontal north-south tracking/east-west axis azimuth.

        :returns: Surface azimuth.
        :rtype: (sequence of) :py:class:`float`
        """
        return (0. if xrf.fabs(self.sc.azimuth) < np.pi / 2 else np.pi)

    def ew_track_tilt(self):
        """Get horizontal east-west tracking/north-south axis tilt.

        :returns: Surface tilt.
        :rtype: (sequence of) :py:class:`float`
        """
        return xrf.atan(
            xrf.tan(self.sc.zenith)
            * xrf.fabs(xrf.cos(self.ew_track_azimuth() - self.sc.azimuth)))

    def ew_track_azimuth(self):
        """Get horizontal east-west tracking/north-south axis azimuth.

        :returns: Surface azimuth.
        :rtype: (sequence of) :py:class:`float`
        """
        return (1. if self.sc.azimuth > 0 else -1.) * np.pi / 2

    def vertical_track_tilt(self):
        """Get vertical-axes tracking tilt.

        :returns: Surface tilt.
        :rtype: (sequence of) :py:class:`float`
        """
        return self._surface_tilt

    def vertical_track_azimuth(self):
        """Get vertical-axes tracking azimuth.

        :returns: Surface azimuth.
        :rtype: (sequence of) :py:class:`float`
        """
        return self.sc.azimuth

    def two_track_tilt(self):
        """Get two-axes tracking tilt.

        :returns: Surface tilt.
        :rtype: (sequence of) :py:class:`float`
        """
        return self.sc.zenith

    def two_track_azimuth(self):
        """Get two-axes tracking azimuth.

        :returns: Surface azimuth.
        :rtype: (sequence of) :py:class:`float`
        """
        return self.sc.azimuth

    def none_track_tilt(self):
        """No-tracking tilt.

        :returns: Surface tilt.
        :rtype: (sequence of) :py:class:`float`
        """
        return self._surface_tilt

    def none_track_azimuth(self):
        """No-tracking azimuth.

        :returns: Surface azimuth.
        :rtype: (sequence of) :py:class:`float`
        """
        return self._surface_azimuth
