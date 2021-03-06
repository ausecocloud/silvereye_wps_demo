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
    def year_as_monthly_vector(year: int) -> List[str]:
        """
        Converts a given time range into a list of iso strings per month
        Example: f(1995) -> ['1995-01', '1995-02', ..., '1995-12']
        :param year: year in range 1970..2014
        :return: a List of strings
        """
        mo_range = range(1, 13)
        return ["{:04d}-{:02d}".format(year, mo) for mo in mo_range]

    @staticmethod
    def year_months_as_vector(year: int, mo_range: Tuple[int, int]) -> List[str]:
        """
        Converts a given time range into a list of iso strings per month
        Example: f(1995, (2, 4)) -> ['1995-02', '1995-03', '1995-04']
        :param year: year in range 1970..2014
        :param mo_range: range of months, each month in range 1..12
        :return: a List of strings
        """
        (mo_min, mo_max) = mo_range
        r = range(mo_min, mo_max + 1)
        return ["{:04d}-{:02d}".format(year, mo) for mo in r]

    @staticmethod
    def years_as_monthly_vector(yr_range: Tuple[int, int]) -> List[str]:
        """
        Converts a given time range into a list of iso strings per month
        Example: f((2001, 2003)) -> ['2001-01', ..., '2001-12',
                                     '2002-01', ..., '2002-12',
                                     '2003-01', ..., '2003-12']
        :param yr_range: years in range 1970..2014
        :return: a NumPy Array of strings
        """
        (yr_lo, yr_hi) = yr_range
        years_range = range(yr_lo, yr_hi + 1)
        mo_range = range(1, 13)
        return ["{:04d}-{:02d}".format(yr, mo) for yr in years_range for mo in mo_range]

    @staticmethod
    def years_month_as_vector(yr_range: Tuple[int, int], mo: int) -> List[str]:
        """
        Converts a given year range into a list of iso strings with only one month per year.
        Example: f((1991, 1995), 2) -> ['1991-02', '1992-02', '1993-02', '1994-02', '1995-02']
        :param yr_range: years in range 1970..2014
        :param mo: desired month in range 1..12
        :return: a NumPy Array of strings
        """
        (yr_lo, yr_hi) = yr_range
        years_range = range(yr_lo, yr_hi + 1)
        return ["{:04d}-{:02d}".format(yr, mo) for yr in years_range]

    @staticmethod
    def year_as_quarterly_vector(year: int) -> List[str]:
        """
        Converts a given year into a list of iso strings per quarter.
        Example: f(1990) -> ["1990-q1", "1990-q2", "1990-q3", "1990-q4"]
        :param year: year in range 1970..2014
        :return: a List of strings
        """
        quarters_range = range(1, 5)
        return ["{:04d}-q{:1d}".format(year, qt) for qt in quarters_range]

    @staticmethod
    def years_as_quarterly_vector(yr_range: Tuple[int, int]) -> List[str]:
        """
        Converts a given year range into a list of iso strings will all quarters per year.
        Example: f((1990,1991)) -> ["1990-q1", "1990-q2", "1990-q3", "1990-q4",
                                    "1991-q1", "1991-q2", "1991-q3", "1991-q4"]
        :param yr_range: range of years within 1970..2014
        :return: a List of strings
        """
        (yr_lo, yr_hi) = yr_range
        years_range = range(yr_lo, yr_hi + 1)
        quarters_range = range(1, 5)
        return ["{:04d}-q{:1d}".format(yr, qt) for yr in years_range for qt in quarters_range]

    @staticmethod
    def years_quarter_as_vector(yr_range: Tuple[int, int], qt: int) -> List[str]:
        """
        Converts a given year range into a list of iso strings with one quarter each.
        Example: f((1990,1992), 3) -> ["1990-q3", "1991-q3", "1992-q3"]
        :param yr_range: years in range 1970..2014
        :param qt: desired quarter
        :return: a List of strings
        """
        (yr_lo, yr_hi) = yr_range
        r = range(yr_lo, yr_hi + 1)
        return ["{:04d}-q{:1d}".format(yr, qt) for yr in r]

    @staticmethod
    def years_as_vector(year_range: Tuple[int, int]) -> List[str]:
        """
        Converts a given year range into a list of iso strings per year
        Example: f((2001, 2003)) -> ['2001', '2002', '2003']
        :param year_range: years in range 1970..2014
        :return: a NumPy Array of strings
        """
        (yr_lo, yr_hi) = year_range
        r = range(yr_lo, yr_hi + 1)
        return ["{:04d}".format(yr) for yr in r]

    @staticmethod
    def fromto_yrmo_as_vector(yrmo_from: Tuple[int, int],
                              yrmo_to: Tuple[int, int]) -> List[Tuple[int, int]]:
        (yr_from, mo_from) = yrmo_from
        (yr_to, mo_to) = yrmo_to

        if yr_from == yr_to:
            mo_same_year_range = range(mo_from, mo_to + 1)
            return [(yr_from, mo) for mo in mo_same_year_range]
        else:
            result = []
            # first year
            mo_first_year_range = range(mo_from, 13)
            result.append([(yr_from, mo) for mo in mo_first_year_range])
            # intermediate whole years
            whole_year_range = range(yr_from + 1, yr_to)
            for yr in whole_year_range:
                whole_mo_range = range(1, 13)
                result.append([(yr, mo) for mo in whole_mo_range])
            # last year
            mo_last_year_range = range(1, mo_to + 1)
            result.append([(yr_to, mo) for mo in mo_last_year_range])
            # flatten list
            return [item for sublist in result for item in sublist]

    @staticmethod
    def fromto_yrmo_as_string_vector(yrmo_from: Tuple[int, int],
                                     yrmo_to: Tuple[int, int]) -> List[str]:
        (yr_from, mo_from) = yrmo_from
        (yr_to, mo_to) = yrmo_to

        if yr_from == yr_to:
            mo_same_year_range = range(mo_from, mo_to + 1)
            return ["{:04d}-{:02d}".format(yr_from, mo) for mo in mo_same_year_range]
        else:
            result = []
            # first year
            mo_first_year_range = range(mo_from, 13)
            result.append(["{:04d}-{:02d}".format(yr_from, mo) for mo in mo_first_year_range])
            # intermediate whole years, if any
            whole_year_range = range(yr_from + 1, yr_to)
            for yr in whole_year_range:
                whole_mo_range = range(1, 13)
                result.append(["{:04d}-{:02d}".format(yr, mo) for mo in whole_mo_range])
            # last year
            mo_last_year_range = range(1, mo_to + 1)
            result.append(["{:04d}-{:02d}".format(yr_to, mo) for mo in mo_last_year_range])
            # flatten list
            return [item for sublist in result for item in sublist]


if __name__ == '__main__':
    pass
    # v = Indexers.lat_as_vector((-28.985, -27.925))
    # v = Indexers.lon_as_vector((153.1935, 153.5335))
    # v = Indexers.year_as_monthly_vector(1990)
    # v = Indexers.years_as_monthly_vector((1990, 1992))
    # v = Indexers.years_quarter_as_vector((2001, 2005), 3)
    # v = Indexers.years_as_quarterly_vector((2001, 2005))
    # v = Indexers.year_as_quarterly_vector(2001)
    # v = Indexers.fromto_yrmo_as_vector((1990, 3), (1992, 7))
    # v = Indexers.fromto_yrmo_as_vector((1990, 10), (1991, 3))
    # print(v)
