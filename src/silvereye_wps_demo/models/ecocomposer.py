import numpy as np
from typing import List, Tuple

from silvereye_wps_demo.models.tempmax import TempMax
from silvereye_wps_demo.models.tempmin import TempMin
from silvereye_wps_demo.models.rainfall import Rainfall
from silvereye_wps_demo.models.vapourpressure import VapourPressure
from silvereye_wps_demo.models.solarradiation import SolarRadiation

from silvereye_wps_demo.models.helpers.indexers import Indexers
from silvereye_wps_demo.models.helpers.validators import Validators
from silvereye_wps_demo.models.helpers.csvarraywriter import CSVArrayWriter


class EcoComposer:

    def __init__(self, variables: List) -> None:
        """initializer"""
        self.variables = variables
        self.instances = {}  # will hold instances of classes, when needed
        if not self._valid_vars():
            raise ValueError("ecoComposer::init: invalid list of variables")
        self._create_instances()

    def _valid_vars(self) -> bool:
        """ensures the requested processes are within our capabilities"""
        valid_vars = [
            "rainfall",
            "solar_radiation",
            "temp_max",
            "temp_min",
            "vapour_pressure"
        ]
        for v in self.variables:
            if v not in valid_vars:
                return False  # quits after not finding one
        return True

    def _create_instances(self) -> None:
        """
        Based on the processes requested,
        creates instances of the EcoMeasure classes that will be used.
        """
        if "temp_max" in self.variables:
            self.instances["temp_max"] = TempMax()

        if "temp_min" in self.variables:
            self.instances["temp_min"] = TempMin()

        if "rainfall" in self.variables:
            self.instances["rainfall"] = Rainfall()

        if "vapour_pressure" in self.variables:
            self.instances["vapour_pressure"] = VapourPressure()

        if "solar_radiation" in self.variables:
            self.instances["solar_radiation"] = SolarRadiation()

    def process_one_year_one_month(self,
                                   file_name: str,
                                   yr: int, mo: int,
                                   lat_range: Tuple[float, float],
                                   lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a given year-month period
        :param file_name: path to outfile file to write into
        :param yr: year in range 1970..2014
        :param mo: month in range 1..12
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        is_valid = len((self.instances.keys())) > 0 \
                   and Validators.is_valid_year(yr) \
                   and Validators.is_valid_month(mo) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer.process_one_year_one_month(): Invalid parameters")

        # make the latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        report = [np.repeat(lat_col, lon_size), np.tile(lon_col, lat_size)]
        field_names = ["lat", "lon"]

        # now, iterate over variables, and collect results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_by_month(yr, mo, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_one_year_all_months(self,
                                    file_name: str,
                                    yr: int,
                                    lat_range: Tuple[float, float],
                                    lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a whole year period, getting by month
        :param file_name: path to output file to write into
        :param yr: year in range 1970..2014
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year(yr) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer.process_one_year_all_months(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.year_as_monthly_vector(yr)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)  # should be 12

        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year-month", "lat", "lon"]

        # now, perform each process, and accum results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_one_year_all_months(yr, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_years_all_months(self,
                                 file_name: str,
                                 yr_range: Tuple[int, int],
                                 lat_range: Tuple[float, float],
                                 lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a whole year period, getting by month
        :param file_name: path to file where the results will be written
        :param yr_range: year range in range 1970..2014
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year_range(yr_range)\
                   and Validators.is_valid_range(lat_range, "lat")\
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer.process_years_all_months(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.years_as_monthly_vector(yr_range)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)  # should be 12 * (number of years)

        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year-month", "lat", "lon"]

        # now, iterate over processes, perform each process, and accum results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_years_all_months(yr_range, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_years_one_month(self,
                                file_name: str,
                                yr_range: Tuple[int, int],
                                mo: int,
                                lat_range: Tuple[float, float],
                                lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a whole year period, getting by month
        :type lat_range: Tuple[float, float]
        :param file_name: path to output file to write into
        :param yr_range: year range in range 1970..2014
        :param mo: one month in range 1..12
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year_range(yr_range) \
                   and Validators.is_valid_month(mo) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer::process_years_one_month(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.years_month_as_vector(yr_range, mo)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)  # should be (number of years) * 1 month
        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year-month", "lat", "lon"]

        # now, iterate over processes, perform each process, and accum results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_years_one_month(yr_range, mo, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_one_year_one_quarter(self,
                                     file_name: str,
                                     yr: int, qtr: int,
                                     lat_range: Tuple[float, float],
                                     lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a given year-month period
        :param file_name: path to output file to write into
        :param yr: year in range 1970..2014
        :param qtr: quarter in range 1..4
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        is_valid = len((self.instances.keys())) > 0 \
                   and Validators.is_valid_year(yr) \
                   and Validators.is_valid_quarter(qtr) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer.process_one_year_one_quarter(): Invalid parameters")

        # make the latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        lat_size = len(lat_col)
        lon_size = len(lon_col)

        report = [np.repeat(lat_col, lon_size), np.tile(lon_col, lat_size)]
        field_names = ["lat", "lon"]

        # now, iterate over processes, perform each process, and accum results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_by_quarter(yr, qtr, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_one_year_all_quarters(self,
                                      file_name: str,
                                      yr: int,
                                      lat_range: Tuple[float, float],
                                      lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a whole year period, by quarter
        :param file_name: path to output file to write into
        :param yr: year in range 1970..2014
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs to csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year(yr) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer::process_one_year_all_quarters(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.year_as_quarterly_vector(yr)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)  # should be 4
        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year-quarter", "lat", "lon"]

        # now, iterate process over variables, and collect results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_one_year_all_quarters(yr, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_years_all_quarters(self,
                                   file_name: str,
                                   yr_range: Tuple[int, int],
                                   lat_range: Tuple[float, float],
                                   lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a whole year period, by quarters
        :param file_name: path to output file to write into
        :param yr_range: year range in 1970..2014
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year_range(yr_range) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer::process_years_all_quarters(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.years_as_quarterly_vector(yr_range)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)  # should be 4 * (number of years)

        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year-quarter", "lat", "lon"]

        # now, iterate over processes, perform each process, and accum results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_years_all_quarters(yr_range, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_years_one_quarter(self,
                                  file_name: str,
                                  yr_range: Tuple[int, int],
                                  qtr: int,
                                  lat_range: Tuple[float, float],
                                  lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a whole year period, getting by month
        :param file_name: name of output file to write into
        :param yr_range: year range in range 1970..2014
        :param qtr: one quarter in range 1..4
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year_range(yr_range) \
                   and Validators.is_valid_quarter(qtr) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer::process_years_one_quarter(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.years_quarter_as_vector(yr_range, qtr)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)  # should be (number of years) * 1 quarter

        # prepare report series columns, and header
        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year-quarter", "lat", "lon"]

        # now, iterate process over variables, and collect results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_years_one_quarter(yr_range, qtr, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_one_year_month_range(self,
                                 file_name: str,
                                 yr: int,
                                 mo_range: Tuple[int, int],
                                 lat_range: Tuple[float, float],
                                 lon_range: Tuple[float, float]):
        """
        processes the monthly mean for a range of months, in one year
        :param file_name: path to output file to write into
        :param yr: year in range 1970..2014
        :param mo_range: range of months, each in range 1..12
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year(yr) \
                   and Validators.is_valid_range(mo_range, "mo") \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer::process_one_year_month_range(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.year_months_as_vector(yr, mo_range)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)

        # prepare report series columns, and headers
        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year-month", "lat", "lon"]

        # now, process variables, and collect results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_one_year_month_range(yr, mo_range, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_one_year(self,
                         file_name: str,
                         yr: int,
                         lat_range: Tuple[float, float],
                         lon_range: Tuple[float, float]) -> None:
        """
        processes the mean for a whole year period, by year
        :param file_name: path to output file to write into
        :param yr: year in range 1970..2014
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs to csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year(yr) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer::process_one_year(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = ["{:04d}".format(yr)]  # only one element
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)  # should be 1
        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year", "lat", "lon"]

        # now, iterate process over variables, and collect results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_by_year(yr, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_years(self,
                      file_name: str,
                      yr_range: Tuple[int, int],
                      lat_range: Tuple[float, float],
                      lon_range: Tuple[float, float]) -> None:
        """
        processes the means for a range of years, by year
        :param file_name: path to output file to write into
        :param yr_range: range of years, with each in range 1970..2014
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs to csv file
        """
        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year_range(yr_range) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer::process_years(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.years_as_vector(yr_range)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)  # should be 1
        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year", "lat", "lon"]

        # now, iterate process over variables, and collect results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_years(yr_range, lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()

    def process_fromto_year_month_range(self,
                                        file_name: str,
                                        yrmo_from: Tuple[int, int],
                                        yrmo_to: Tuple[int, int],
                                        lat_range: Tuple[float, float],
                                        lon_range: Tuple[float, float]):
        """
        processes the monthly means for a range of months, within years
        :param file_name: path to output file to write into
        :param yrmo_from: starting year-month tuple, with year in range 1970:2014 and month in 1:12
        :param yrmo_to: ending year-month tuple, with year in range 1970:2014 and month in 1:12
        :param lat_range: latitudes
        :param lon_range: longitudes
        :return: None, outputs a csv file
        """
        (yr_from, mo_from) = yrmo_from
        (yr_to, mo_to) = yrmo_to

        is_valid = len(self.instances.keys()) > 0 \
                   and Validators.is_valid_year(yr_from) \
                   and Validators.is_valid_year(yr_to) \
                   and yr_from <= yr_to \
                   and Validators.is_valid_month(mo_from) \
                   and Validators.is_valid_month(mo_to) \
                   and Validators.is_valid_range(lat_range, "lat") \
                   and Validators.is_valid_range(lon_range, "lon")
        if not is_valid:
            raise ValueError("ecoComposer::process_fromto_year_month_range(): Invalid parameters")

        # make the time, latitude and longitude columns
        lat_col = Indexers.lat_as_vector(lat_range)
        lon_col = Indexers.lon_as_vector(lon_range)
        time_col = Indexers.fromto_yrmo_as_string_vector(yrmo_from, yrmo_to)
        lat_size = len(lat_col)
        lon_size = len(lon_col)
        time_size = len(time_col)

        # prepare report series columns, and headers
        report = [
            np.repeat(time_col, lat_size * lon_size),
            np.tile(np.repeat(lat_col, lon_size), time_size),
            np.tile(lon_col, lat_size * time_size)]
        field_names = ["year-month", "lat", "lon"]

        # now, process variables, and collect results
        for v in self.variables:
            field_names.append(self.instances[v].column_name())
            result = self.instances[v].mean_fromto_year_month_range(yrmo_from, yrmo_to,
                                                                    lat_range, lon_range)
            report.append(result.flatten())

        # report[j] with 0 < j < total_cols has all the data, by column
        csv = CSVArrayWriter(file_name, field_names, report)
        csv.write()
