from typing import Tuple, List
import numpy as np

import silvereye_wps_demo.models.ecoconstants as eco_constants


class Indexers(object):
    """
    Functions to retrieve the numerical index into the array, given its value.
    Because the data is linear, there is no lookup involved, only offset calculations, which are very quick.
    """
    @staticmethod
    def get_lat_idx(lat: float) -> int:
        """
        Returns the index for a given latitude,
        on the latitude array.
        """
        idx = -1
        lat = abs(lat)         # reverse the sign
        if eco_constants.LAT_MIN == lat:
            idx = eco_constants.LAT_IDX_MIN
        elif eco_constants.LAT_MAX == lat:
            idx = eco_constants.LAT_IDX_MAX
        elif eco_constants.LAT_MIN < lat < eco_constants.LAT_MAX:
            idx = round((lat - eco_constants.LAT_MIN) / eco_constants.LAT_DELTA)
        return idx

    @staticmethod
    def get_lon_idx(lon: float) -> int:
        """
        Returns the index for a given longitude,
        on the longitude array.
        """
        idx = -1
        if eco_constants.LON_MIN == lon:
            idx = eco_constants.LON_IDX_MIN
        elif eco_constants.LON_MAX == lon:
            idx = eco_constants.LON_IDX_MAX
        elif (eco_constants.LON_MIN < lon < eco_constants.LON_MAX):
            idx = round((lon - eco_constants.LON_MIN)/eco_constants.LON_DELTA)
        return idx

    @staticmethod
    def get_time_idx(t: float) -> int:
        """Given a date t, expressed in seconds,
           in range 1970-01-01 to 2014-12-31,
           returns the index on the time array.
        """
        idx = -1
        if eco_constants.TIME_MIN == t:
            idx = eco_constants.TIME_IDX_MIN
        elif eco_constants.TIME_MAX == t:
            idx = eco_constants.TIME_IDX_MAX
        elif eco_constants.TIME_MIN < t < eco_constants.TIME_MAX:
            idx = round((t - eco_constants.TIME_MIN)/eco_constants.TIME_DELTA)
        return idx

    @staticmethod
    def lat_as_vector(lat_range: Tuple[float, float]):
        """
        Converts a tuple range of latitudes into an explicit array of values.
        NOTE: All latitudes in Australia have negative values, and the order is reversed;
        i.e. when listing them as a vector, values closer to the Equator come first.
        :param lat_range: Tuple[float, float]
        :return: NPArray with result
        """
        (lat_lo_neg, lat_hi_neg) = lat_range
        lat_lo = -lat_hi_neg
        lat_hi = -lat_lo_neg
        lat_size = int((lat_hi - lat_lo) / eco_constants.LAT_DELTA) + 2
        v = np.linspace(start=lat_lo, stop=lat_hi, num=lat_size) * (-1)
        return [round(n, 3) for n in v]

    @staticmethod
    def lon_as_vector(lon_range: Tuple[float, float]):
        """
        Converts a tuple range of longitudes into an explicit array of values.
        NOTE: All longitudes in Australia have positive values.
        :param lon_range: Tuple[float, float]
        :return: NPArray with result
        """
        (lon_lo, lon_hi) = lon_range
        lon_size = int((lon_hi - lon_lo) / eco_constants.LON_DELTA) + 1
        v = np.linspace(start=lon_lo, stop=lon_hi, num=lon_size)
        return [round(n, 3) for n in v]

    @staticmethod
    def year_as_monthly_vector(year: int):
        """
        Converts a given time range into a list of iso strings per month
        Example: f(1995) -> ['1995-01', '1995-02', ..., '1995-12']
        :param year: year in range 1970..2014
        :return: a NumPy Array of strings
        """
        vector = []
        for mo in range(1, 13):
            vector.append("{:04d}-{:02d}".format(year, mo))
        return vector

    @staticmethod
    def year_months_as_vector(year: int, mo_range: Tuple[int, int]):
        """
        Converts a given time range into a list of iso strings per month
        Example: f(1995) -> ['1995-01', '1995-02', ..., '1995-12']
        :param year: year in range 1970..2014
        :return: a NumPy Array of strings
        """
        (mo_min, mo_max) = mo_range
        vector = []
        for mo in range(mo_min, mo_max + 1):
            vector.append("{:04d}-{:02d}".format(year, mo))
        return vector

    @staticmethod
    def years_as_monthly_vector(year_range: Tuple[int, int]):
        """
        Converts a given time range into a list of iso strings per month
        Example: f((2001, 2003)) -> ['2001-01', ..., '2001-12',
                                     '2002-01', ..., '2002-12',
                                     '2003-01', ..., '2003-12']
        :param year_range: years in range 1970..2014
        :return: a NumPy Array of strings
        """
        vector = []
        (yr_lo, yr_hi) = year_range
        for yr in range(yr_lo, yr_hi + 1):
            for mo in range(1, 13):
                vector.append("{:04d}-{:02d}".format(yr, mo))
        return vector

    @staticmethod
    def years_month_as_vector(year_range: Tuple[int, int], mo: int):
        """
        Converts a given year range into a list of iso strings with only one month per year.
        Example: f((1991, 1995), 2) -> ['1991-02', '1992-02', '1993-02', '1994-02', '1995-02']
        :param year_range: years in range 1970..2014
        :param mo: desired month in range 1..12
        :return: a NumPy Array of strings
        """
        vector = []
        (yr_lo, yr_hi) = year_range
        for yr in range(yr_lo, yr_hi + 1):
            vector.append("{:04d}-{:02d}".format(yr, mo))
        return vector

    @staticmethod
    def year_as_quarterly_vector(year: int) -> List:
        """
        Converts a given year into a list of iso strings per quarter.
        Example: f(1990) -> ["1990-q1", "1990-q2", "1990-q3", "1990-q4"]
        :param year: year in range 1970..2014
        :return: a List of strings
        """
        vector = []
        for qt in range(1, 5):
            vector.append("{:04d}-q{:1d}".format(year, qt))
        return vector

    @staticmethod
    def years_as_quarterly_vector(yr_range: Tuple[int, int]) -> List:
        """
        Converts a given year range into a list of iso strings will all quarters per year.
        Example: f((1990,1991)) -> ["1990-q1", "1990-q2", "1990-q3", "1990-q4",
                                    "1991-q1", "1991-q2", "1991-q3", "1991-q4"]
        :param yr_range: range of years within 1970..2014
        :return: a List of strings
        """
        vector = []
        (yr_lo, yr_hi) = yr_range
        for yr in range(yr_lo, yr_hi + 1):
            for qt in range(1, 5):
                vector.append("{:04d}-q{:1d}".format(yr, qt))
        return vector

    @staticmethod
    def years_quarter_as_vector(yr_range: Tuple[int, int], qt: int) -> List:
        """
        Converts a given year range into a list of iso strings with one quarter each.
        Example: f((1990,1992), 3) -> ["1990-q3", "1991-q3", "1992-q3"]
        :param yr_range: years in range 1970..2014
        :param qt: desired quarter
        :return: a List of strings
        """
        vector = []
        (yr_lo, yr_hi) = yr_range
        for yr in range(yr_lo, yr_hi + 1):
            vector.append("{:04d}-q{:1d}".format(yr, qt))
        return vector

    @staticmethod
    def years_as_vector(year_range: Tuple[int, int]):
        """
        Converts a given year range into a list of iso strings per year
        Example: f((2001, 2003)) -> ['2001', '2002', '2003']
        :param year_range: years in range 1970..2014
        :return: a NumPy Array of strings
        """
        (yr_lo, yr_hi) = year_range
        return ["{:04d}".format(yr) for yr in range(yr_lo, yr_hi + 1)]

if __name__ == '__main__':
    # v = Indexers.lat_as_vector((-28.985, -27.925))
    # v = Indexers.lon_as_vector((153.1935, 153.5335))
    # v = Indexers.year_as_monthly_vector(1990)
    # v = Indexers.years_as_monthly_vector((1990, 1992))
    # v = Indexers.years_quarter_as_vector((2001, 2005), 3)
    # v = Indexers.years_as_quarterly_vector((2001, 2005))
    v = Indexers.year_as_quarterly_vector(2001)
    print(v)
