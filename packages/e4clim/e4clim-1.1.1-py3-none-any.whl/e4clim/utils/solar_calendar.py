"""Calculations related to calendars and astronomical parameters."""
import numpy as np
import xarray as xr
import xarray.ufuncs as xrf

#: Variable long-names.
LONG_NAMES = {
    'julian_day': 'Julian Day',
    'ndays_since': 'Days since 2000-01-01 12:00:00',
    'mean_longitude': 'Mean Longitude',
    'elevation': 'Elevation', 'zenith': 'Zenith',
    'azimuth': 'Azimuth',
    'mean_anomaly': 'Mean Anomaly',
    'ecliptic_longitude': 'Ecliptic Longitude',
    'ecliptic_obliquity': 'Obliquity of Ecliptic',
    'right_ascension': 'Right Ascension',
    'declination': 'Declination',
    'utc_hour': 'Hour UTC',
    'greenwich_mean_sideral_time': 'Greenwich Mean Sideral Time',
    'local_mean_sideral_time': 'Local Mean Sideral Time',
    'hour_angle': 'Hour Angle',
    'sunset_hour_angle': 'Sunset Hour Angle',
    'daily_cos_zenith': 'Daily-Integrated Cosine of Zenith',
    'daily_mean_cos_zenith': 'Daily-Averaged Cosine of Zenith'
}


def _compute_if_none(fun):
    """Compute attribute with the same name as :py:obj:`fun`
    only if `None`."""

    def comp_fun(self):
        attr_name = '_' + fun.__name__

        # Compute variable only if None
        if getattr(self, attr_name) is None:
            # Compute variable
            var = fun(self)

            # Make sure it is a data array
            try:
                var = xr.DataArray(var, coords=[('time', self.time)])
            except ValueError:
                var = xr.DataArray(var)

            # Add variable to attribute
            setattr(self, attr_name, var)

            # Add names
            self._add_attributes(attr_name)

        return getattr(self, attr_name)

    return comp_fun


def _clip_angle(angle):
    """Clip angle so that: math: `-\pi ^\\circ <= \\theta < \pi ^\\circ`.

    :param angle: Angle in radians.
    :type angle: (sequence of) :py:class:`float`

    :returns: Clipped angle.
    :rtype: (sequence of) :py:class:`float`
    """
    lim = np.pi
    return xrf.fabs(xrf.fmod(angle + lim, 2 * lim)) - lim


class SolarCalendarComputer(object):
    """Class to compute solar calendar variables.
    When getting an attribute, the variable
    corresponding to it is automatically computed. New computations are
    only performed if the needed attribute value is `None`, i.e. if it
    has not previously been computed.
    To perform new computations, start from a new object,
    or call :py:meth:`clear`.

    .. note::
      * The Almanac approximation is used with ecliptic coordinates,
        as in Michalsky (1988).
      * The *solar elevation* is the angle between the horizontal and the
        line to the sun, that is, the complement of the *zenith angle*.
      * The *solar azimuth* is the angular displacement from south of the
        projection of beam radiation on the horizontal plane. Displacements
        east of south are negative and west of south are positive.
      * The *right ascension* is the angular distance measured eastward
        along the celestial equator from the Sun at the March equinox
        to the hour circle of the point above the earth in question.
      * The *declination* is the angular position of the sun at solar noon
        (i.e., when the sun is on the local meridian)
        with respect to the plane of the equator, north positive;
        :math:`−23.45^\circ \le \delta \le 23.45^\circ`.
      * The *hour angle* is the angular displacement of the sun east or west
        of the local meridian due to rotation of the earth on its axis at
        15 degrees per hour; morning negative, afternoon positive.
      * The *sunset hour angle* is the hour angle when elevation is zero.
        See Duffie and Beckman(2013).

    .. warning::
      The Almanac's approximation covers the (1950-2050) period
      and may need to be modified for longer periods.

    .. seealso::
      * Michalsky, J.J., 1988. The Astronomical Almanac's Algorithm format
        Approximate Solar Position (1950, 2050). *Solar Energy* 40, 227-235.
      * Duffie, J.A., Beckman, W.A., 2013.
      * *Solar Energy and Thermal Processes*, fourth ed. Wiley, Hoboken, NJ.

    """

    def __init__(self, time, lat, lon, angles_in_degrees=False):
        """Initialize solar angles computer.

        :param time: Time.
        :param lat: Latitude.
        :param lon: Longitude.
        :param angles_in_degrees: Whether angles are given in degrees instead
          of radians and should be returned in degrees by :py:meth:`get_angle`.
        :type time: (sequence of) datetime.
        :type lat: (sequence of) :py:class:`float`.
        :type lon: (sequence of) :py:class:`float`.
        :type angles_in_degrees: bool

        .. warning::

          * All attribute variables (e.g. :py:attr:`hour_angle`)
            are given in radians, between :py:math:`-\pi` and :py:math:`\pi`,
            and all computations are performed
            in radians. To get angles in the same units as those
            provided to constructor, call :py:meth:`get_angle`.
          * 
        """

        # Manage degrees-radians conversion
        self.angles_in_degrees = angles_in_degrees
        self.fact = np.deg2rad(1.) if self.angles_in_degrees else 1.
        self.inv_fact = 1. if self.angles_in_degrees else np.deg2rad(1.)
        self.angle_units = 'degrees' if self.angles_in_degrees else 'radians'

        # Convert to radians if needed
        self.time = time
        self.lat = lat * self.fact
        self.lon = lon * self.fact

        # Initialize all variables to be computed to None
        self.clear()

    def clear(self):
        """Set all computed attribute variables to `None`."""
        for variable_name in LONG_NAMES:
            setattr(self, '_' + variable_name, None)

    def _add_attributes(self, variable_name):
        """Add `long_name` and `units` attributes to data array.

        :param variable_name: Variable name.
        :type variable_name: str
        """
        # Get variable from variable name
        var = getattr(self, variable_name)

        # Try to add attributes
        try:
            variable_name = (variable_name[1:] if variable_name[0] == '_' else
                             variable_name)
            var.attrs['long_name'] = LONG_NAMES[variable_name]
            var.attrs['units'] = self.angle_units
        except AttributeError:
            pass

    def get_angle(self, angle_name):
        """Get angle, converted in degrees if needed.

        :param angle_name: Angle name.
        :type angle_name: str

        .. warning:: No exception is raised if a non-angle variable name,
          e.g. :py:attr:`julian_day` is given, leading to return this variable
          after a potential spurious angle conversion. Instead, such variables
          should directly be accessed as attribute.
        """
        return _clip_angle(getattr(self, angle_name)) / self.fact

    @property
    @_compute_if_none
    def julian_day(self):
        """Get Julian day as data array."""
        return self.time.to_julian_date()

    @property
    @_compute_if_none
    def ndays_since(self):
        """Get number of days since 2000-01-01 12:00:00."""
        return self.julian_day - 2451545.0

    @property
    @_compute_if_none
    def mean_longitude(self):
        """Get mean longitude :py:math:`-\pi <= mean_lon <= \pi`."""
        return 4.89495 + 0.01720279 * self.ndays_since

    @property
    @_compute_if_none
    def elevation(self):
        """Compute solar elevation from Julian day, East longitude and
        latitude. Angular extent of sun neglected.
        """
        # Elevation (radians)
        return xrf.arcsin(
            xrf.sin(self.declination) * xrf.sin(self.lat) +
            xrf.cos(self.declination) * xrf.cos(self.lat) *
            xrf.cos(self.hour_angle))

    @property
    @_compute_if_none
    def zenith(self):
        """Get zenith from elevation angle."""
        return np.pi/2 - self.elevation

    @property
    @_compute_if_none
    def azimuth(self):
        """Compute solar azimuth from Julian day, East longitude and latitude.
        Angular extent of sun neglected.
        """
        # Azimuth (radians)
        # Numerical errors may lead to absolute sine values slighly larger
        # than 1. In this case, angle is set to -pi/2, as should be.
        var = -np.pi/2 * xr.ones_like(self.elevation)
        val = (-xrf.cos(self.declination) * xrf.sin(self.hour_angle)
               / xrf.cos(self.elevation))
        xrf.arcsin(val, out=var.values, where=(xrf.fabs(val) < 1.))

        # Assign correct quadrant to azimuth (check discontinuity)
        elc = xrf.arcsin(xrf.sin(self.declination) / xrf.sin(self.lat))
        var = xr.where(self.elevation >= elc, np.pi - var, var)

        return var

    @property
    @_compute_if_none
    def mean_anomaly(self):
        """Get mean anomaly."""
        return 6.24004 + 0.01720197 * self.ndays_since

    @property
    @_compute_if_none
    def ecliptic_longitude(self):
        """Get ecliptic longitude."""
        return self.mean_longitude + 0.03342 * xrf.sin(
            self.mean_anomaly) + 0.00035 * xrf.sin(2 * self.mean_anomaly)

    @property
    @_compute_if_none
    def ecliptic_obliquity(self):
        """Get ecliptic obliquity."""
        return 0.40908 - 7.e-9 * self.ndays_since

    @property
    @_compute_if_none
    def right_ascension(self):
        """Get right ascension."""
        return xrf.arctan2(
            xrf.cos(self.ecliptic_obliquity) *
            xrf.sin(self.ecliptic_longitude),
            xrf.cos(self.ecliptic_longitude))

    @property
    @_compute_if_none
    def declination(self):
        """Get declination."""
        return xrf.arcsin(
            xrf.sin(self.ecliptic_obliquity) *
            xrf.sin(self.ecliptic_longitude))

    @property
    @_compute_if_none
    def utc_hour(self):
        """Get UTC hour in radians."""
        # A decimal part of the Julian date equal to zero
        # corresponds to noon (12h)
        djd = self.julian_day.astype(int)
        return (self.julian_day - djd) * 2*np.pi + np.pi

    @property
    @_compute_if_none
    def greenwich_mean_sideral_time(self):
        """Get Greenwich mean sideral time."""
        return 1.753369 + 0.0172027917 * self.ndays_since + self.utc_hour

    @property
    @_compute_if_none
    def local_mean_sideral_time(self):
        """Get local mean sideral time."""
        return self.greenwich_mean_sideral_time + self.lon

    @property
    @_compute_if_none
    def hour_angle(self):
        """Get hour angle in radians."""
        return self.local_mean_sideral_time - self.right_ascension

    @property
    @_compute_if_none
    def sunset_hour_angle(self):
        """Compute sunset hour angle from latitude and declination."""
        # Compute sunset hour angle
        return xrf.arccos(
            -xrf.tan(self.lat) * xrf.tan(self.declination))

    @property
    @_compute_if_none
    def daily_cos_zenith(self):
        """Get daily-integrated cosine of zenith angle."""
        return ((
            self.sunset_hour_angle * xrf.sin(self.declination)
            * xrf.sin(self.lat) + xrf.cos(self.declination) * xrf.cos(self.lat)
            * xrf.sin(self.sunset_hour_angle))
            * 2 * (12. / np.pi))

    @property
    @_compute_if_none
    def daily_mean_cos_zenith(self):
        """Get daily-averaged cosine of zenith angle."""
        return xr.where(
            xrf.fabs(self.sunset_hour_angle) > 1.e-8,
            self.daily_cos_zenith / (2 * (12. / np.pi))
            / self.sunset_hour_angle, 0.)
