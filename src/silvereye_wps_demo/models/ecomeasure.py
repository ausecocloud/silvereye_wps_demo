from pydap.client import open_url
from typing import Tuple
import numpy as np

from silvereye_wps_demo.models.helpers.validators import Validators
from silvereye_wps_demo.models.helpers.indexers import Indexers
from silvereye_wps_demo.models.helpers.timeconverters import TimeConverters


class EcoMeasure(object):
    """
    Generic EcoMeasure object.
    Do not instantiate directly.
    Parent of TempMax, TempMin, Rainfall,
    VapourPressure and SolarRadiation classes.
    """
    def __init__(self, url: str, variable: str, name: str):
        """Initializer, sets the data structures for the class."""
        self.data = {
            'url':  url,
            'variable': variable,
            'name': name,
            'ds': open_url(url, output_grid=False, timeout=3600)
        }
        self.debug = {
            'time_size': 0,
            'lat_size': 0,
            'lon_size': 0,
            'dimensions': (0, 0, 0),
            'total_size': 0
        }

    def ds(self):
        """Return the dataset. """
        return self.data['ds']

    def raw_data(self):
        """Returns the raw data matrix for this variable"""
        return self.data['ds'][self.data['variable']]

    def column_name(self):
        return self.data["name"]

    def slice(self,
              time_range: Tuple[str, str],
              lat_range: Tuple[float, float],
              lon_range: Tuple[float, float]):
        """
        :param time_range: (time_lo, time_hi)
        time_lo, time_hi :: date strings in iso format

        :param lat_range: (lat_lo, lat_hi)
        lat_lo, lat_hi :: latitudes

        :param lon_range: (lon_lo, lon_hi)
        lon_lo, lon_hi :: longitudes

        :return: NumPy.Array (of 3 dimensions: time, lat, lon) with the result

        throws Exception if any parameter is invalid.

        Example of usage:
        slice = tmax.slice(
                    ('1990-01-01', '1990-01-31'),
                    (-28.16, -27.72),
                    (153.19, 153.53)) # Beenleigh to Coolangatta
        """

        try:
            Validators.validate_parameters(time_range, lat_range, lon_range)  # bombs if error

            # separate low and high parameter values
            (time_lo, time_hi) = time_range
            (lat_lo, lat_hi) = lat_range
            (lon_lo, lon_hi) = lon_range

            # convert times from iso to timestamps
            time_lo_ts = TimeConverters.iso2ts(time_lo)
            time_hi_ts = TimeConverters.iso2ts(time_hi)

            # get time indices
            time_lo_idx = Indexers.get_time_idx(time_lo_ts)
            time_hi_idx = Indexers.get_time_idx(time_hi_ts)

            # get latitude indices
            lat_lo_idx = Indexers.get_lat_idx(lat_lo)
            lat_hi_idx = Indexers.get_lat_idx(lat_hi)

            # get longitude indices
            lon_lo_idx = Indexers.get_lon_idx(lon_lo)
            lon_hi_idx = Indexers.get_lon_idx(lon_hi)

            # debug data
            # time_size = time_hi_idx - time_lo_idx + 1
            # lat_size = abs(lat_hi_idx - lat_lo_idx) + 1
            # lon_size = lon_hi_idx - lon_lo_idx + 1
            # self.debug['time_size'] = time_size
            # self.debug['lat_size'] = lat_size
            # self.debug['lon_size'] = lon_size
            # self.debug['dimensions'] = (time_size, lat_size, lon_size)
            # total_size = time_size * lat_size * lon_size
            # self.debug['total_size'] = total_size
            # self.debug['time_lo_idx'] = time_lo_idx
            # self.debug['time_hi_idx'] = time_hi_idx
            # self.debug['lat_lo_idx'] = lat_lo_idx
            # self.debug['lat_hi_idx'] = lat_hi_idx
            # self.debug['lon_lo_idx'] = lon_lo_idx
            # self.debug['lon_hi_idx'] = lon_hi_idx

            # return slice
            return self.data['ds'][self.data['variable']][
                      time_lo_idx:time_hi_idx,
                      lat_hi_idx:lat_lo_idx,
                      lon_lo_idx:lon_hi_idx
                      ].data
            # for testing without real data:
            # return (np.random.random(total_size) * 30 + 10).reshape(time_size, lat_size, lon_size )

        except ValueError as err:
            print(err)

    def get_debug(self):
        return self.debug

    def mean_by_month(self, year: int, month: int, lat_range: Tuple[float, float], lon_range: Tuple[float, float]):
        """
        Calculates the mean for the given month, for the given coords,
        and returns a 2d matrix with the values.
        :param year: int, in range 1970..2014
        :param month: int, in range 1..12
        :param lat_range: Tuple[float, float], range of latitudes to retrieve
        :param lon_range: Tuple[float, float], range of longitudes to retrieve
        :return: NumPy.Array (of 2 dimensions: lat, lon) with the result
        """
        time_range = TimeConverters.ym2trange(year, month)
        slice = self.slice(time_range, lat_range, lon_range)
        return np.mean(slice, 0)

    def mean_one_year_all_months(self, year: int, lat_range: Tuple[float, float], lon_range: Tuple[float, float]):
        """
        Calculates the means for each month in a given year.
        :param year: in range 1970..2014
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: NumPy array flat
        """
        result = np.array([])
        mo_range = range(1, 13)
        for mo in mo_range:
            mean = self.mean_by_month(year, mo, lat_range, lon_range)
            result = np.concatenate((result, mean.flatten()), axis=0)
        return result

    def mean_years_all_months(self,
                              yr_range: Tuple[int, int],
                              lat_range: Tuple[float, float],
                              lon_range: Tuple[float, float]):
        """
        Calculates the means for a range of years, month by month.
        :param yr_range: year range in 1970..2014
        :param lat_range: latitude range
        :param lon_range: longitude range
        :return: NumPy array flat
        """
        (yr_lo, yr_hi) = yr_range
        result = np.array([])
        years_range = range(yr_lo, yr_hi + 1)
        mo_range = range(1, 13)
        for yr in years_range:
            for mo in mo_range:
                mean = self.mean_by_month(yr, mo, lat_range, lon_range)
                result = np.concatenate((result, mean.flatten()), axis=0)
        return result

    def mean_years_one_month(self,
                             yr_range: Tuple[int, int],
                             mo: int,
                             lat_range: Tuple[float, float],
                             lon_range: Tuple[float, float]):
        """
        Calculates the means for a range of years, for one month.
        :param yr_range: year range in 1970..2014
        :param mo: one month in range 1..12
        :param lat_range: latitude range
        :param lon_range: longitude range
        :return: NumPy array flat
        """
        (yr_lo, yr_hi) = yr_range
        result = np.array([])
        years_range = range(yr_lo, yr_hi + 1)
        for yr in years_range:
            mean = self.mean_by_month(yr, mo, lat_range, lon_range)
            result = np.concatenate((result, mean.flatten()), axis=0)
        return result

    def min_by_month(self,
                     year: int,
                     month: int,
                     lat_range: Tuple[float, float],
                     lon_range: Tuple[float, float]):
        """
        Calculates the minimum for the given month, for the given coords,
        and returns a 2d matrix with the values.
        :param year: int, in range 1970..2014
        :param month: int, in range 1..12
        :param lat_range: Tuple[float, float], range of latitudes to retrieve
        :param lon_range: Tuple[float, float], range of longitudes to retrieve
        :return: NumPy.Array (of 2 dimensions: lat, lon) with the result
        """
        time_range = TimeConverters.ym2trange(year, month)
        slice = self.slice(time_range, lat_range, lon_range)
        return np.ma.min(slice, 0)

    def max_by_month(self,
                     year: int,
                     month: int,
                     lat_range: Tuple[float, float],
                     lon_range: Tuple[float, float]):
        """
        Calculates the maximum for the given month, for the given coords,
        and returns a 2d matrix with the values.
        :param year: int, in range 1970..2014
        :param month: int, in range 1..12
        :param lat_range: Tuple[float, float], range of latitudes to retrieve
        :param lon_range: Tuple[float, float], range of longitudes to retrieve
        :return: NumPy.Array (of 2 dimensions: lat, lon) with the result
        """
        time_range = TimeConverters.ym2trange(year, month)
        slice = self.slice(time_range, lat_range, lon_range)
        return np.ma.max(slice, 0)

    def mean_by_quarter(self,
                        year: int,
                        qtr: int,
                        lat_range: Tuple[float, float],
                        lon_range: Tuple[float, float]):
        """
        Calculates the mean for the given quarter, for the given coords,
        and returns a 2d matrix with the values.
        :param year: in range 1970..2014
        :param qtr: in range 1..4
        :param lat_range: range of latitudes to retrieve
        :param lon_range: range of longitudes to retrieve
        :return: NumPy.Array (of 2 dimensions: lat, lon) with the result
        """
        time_range = TimeConverters.yq2trange(year, qtr)
        slice = self.slice(time_range, lat_range, lon_range)
        return np.mean(slice, 0)

    def mean_one_year_all_quarters(self,
                                   year: int,
                                   lat_range: Tuple[float, float],
                                   lon_range: Tuple[float, float]):
        """
        Calculates the mean for one year, all quarters.
        :param year: year requested in range 1970..2014
        :param lat_range: latitudes in range
        :param lon_range: longitudes range
        :return: NumPy Array flattened to one-dimension vector
        """
        result = np.array([])
        quarters_range = range(1, 5)
        for qtr in quarters_range:
            mean = self.mean_by_quarter(year, qtr, lat_range, lon_range)
            result = np.concatenate((result, mean.flatten()), axis=0)
        return result

    def mean_years_all_quarters(self,
                                yr_range: Tuple[int, int],
                                lat_range: Tuple[float, float],
                                lon_range: Tuple[float, float]):
        """
        Calculates the mean for a range of years, all quarters.
        :param yr_range: year range within 1970..2014
        :param lat_range: latitudes in range
        :param lon_range: longitudes range
        :return: NumPy Array flattened to one-dimensional vector
        """
        (yr_lo, yr_hi) = yr_range
        result = np.array([])
        years_range = range(yr_lo, yr_hi + 1)
        quarters_range = range(1, 5)
        for yr in years_range:
            for qtr in quarters_range:
                mean = self.mean_by_quarter(yr, qtr, lat_range, lon_range)
                result = np.concatenate((result, mean.flatten()), axis=0)
        return result

    def mean_years_one_quarter(self,
                               yr_range: Tuple[int, int],
                               qtr: int,
                               lat_range: Tuple[float, float],
                               lon_range: Tuple[float, float]):
        """
        Calculates the mean for a range of years, one quarter each.
        :param yr_range: year range in range 1970..2014
        :param qtr: desired quarter in range 1..4
        :param lat_range: latitudes in range
        :param lon_range: longitudes range
        :return: NumPy Array flattened to one-dimension vector
        """
        (yr_lo, yr_hi) = yr_range
        result = np.array([])
        years_range = range(yr_lo, yr_hi + 1)
        for yr in years_range:
            mean = self.mean_by_quarter(yr, qtr, lat_range, lon_range)
            result = np.concatenate((result, mean.flatten()), axis=0)
        return result

    def mean_one_year_month_range(self,
                                  year: int,
                                  mo_range: Tuple[int, int],
                                  lat_range: Tuple[float, float],
                                  lon_range: Tuple[float, float]):
        """
        Calculates the means, by month, for a range of months in a given year.
        :param year: in range 1970..2014
        :param mo_range: range of months in range 1..12
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: NumPy array flat
        """
        (mo_min, mo_max) = mo_range
        result = np.array([])
        months_range = range(mo_min, mo_max + 1)
        for mo in months_range:
            mean = self.mean_by_month(year, mo, lat_range, lon_range)
            result = np.concatenate((result, mean.flatten()), axis=0)
        return result

    def mean_by_year(self,
                     year: int,
                     lat_range: Tuple[float, float],
                     lon_range: Tuple[float, float]):
        """
        Calculates the mean for the given year, and returns a 2d matrix with the values.
        :param year: int, in range 1970..2014
        :param lat_range: Tuple[float, float], range of latitudes to retrieve
        :param lon_range: Tuple[float, float], range of longitudes to retrieve
        :return: NumPy.Array (of 2 dimensions: lat, lon) with the result
        """
        time_range = TimeConverters.y2trange(year)
        slice = self.slice(time_range, lat_range, lon_range)
        return np.mean(slice, 0)

    def mean_years(self,
                   yr_range: Tuple[int, int],
                   lat_range: Tuple[float, float],
                   lon_range: Tuple[float, float]):
        """
        Calculates the yearly mean for a range of years, and returns a 2d matrix with the values.
        :param yr_range: range of years, each in range 1970..2014
        :param lat_range: Tuple[float, float], range of latitudes to retrieve
        :param lon_range: Tuple[float, float], range of longitudes to retrieve
        :return: NumPy.Array (of 2 dimensions: lat, lon) with the result
        """
        (yr_min, yr_max) = yr_range
        result = np.array([])
        years_range = range(yr_min, yr_max + 1)
        for yr in years_range:
            mean = self.mean_by_year(yr, lat_range, lon_range)
            result = np.concatenate((result, mean.flatten()), axis=0)
        return result

    def mean_fromto_year_month_range(self,
                                     yrmo_from: Tuple[int, int],
                                     yrmo_to: Tuple[int, int],
                                     lat_range: Tuple[float, float],
                                     lon_range: Tuple[float, float]):
        """
        Calculates the monthly means from year-month to year-month
        :param yrmo_from: starting year-month tuple, with year in range 1970:2014 and month in 1:12
        :param yrmo_to: ending year-month tuple, with year in range 1970:2014 and month in 1:12
        :param lat_range: latitude range
        :param lon_range: longitude range
        :return: NumPy array flat
        """
        result = np.array([])
        range_of_year_months = Indexers.fromto_yrmo_as_vector(yrmo_from, yrmo_to)
        for (yr, mo) in range_of_year_months:
            mean = self.mean_by_month(yr, mo, lat_range, lon_range)
            result = np.concatenate((result, mean.flatten()), axis=0)
        return result
