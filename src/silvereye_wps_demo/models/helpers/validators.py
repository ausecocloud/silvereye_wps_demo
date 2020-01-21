from typing import Tuple
import silvereye_wps_demo.models.ecoconstants as eco_constants


class Validators(object):

    @staticmethod
    def is_valid_range(var_range: Tuple, var_type: str) -> bool:
        """
        validates a (lo, hi) range tuple of type var_type.
        var_type :: "time" | "lat" | "lon"
        returns True if lo < hi"""
        boundaries = {
            "time": {"min": eco_constants.TIME_ISO_MIN, "max": eco_constants.TIME_ISO_MAX},
            "lat": {"min": -eco_constants.LAT_MAX, "max": -eco_constants.LAT_MIN},
            "lon": {"min": eco_constants.LON_MIN, "max": eco_constants.LON_MAX},
            "mo": {"min": eco_constants.MONTH_MIN, "max": eco_constants.MONTH_MAX}
        }
        (lo, hi) = var_range
        return ((boundaries[var_type]["min"] <= lo)
                and (lo < hi)
                and (hi <= boundaries[var_type]["max"]))

    @staticmethod
    def validate_parameters(time_range: Tuple[str, str],
                            lat_range: Tuple[float, float],
                            lon_range: Tuple[float, float]) -> None:
        """
        Validates the parameters:
        time_range, lat_range, lon_range are tuples of (lo, hi) values
        """
        template = "Invalid {} parameters: Values must be min < lo < hi < max."
        if not Validators.is_valid_range(time_range, "time"):
            raise ValueError(template.format("time"))
        if not Validators.is_valid_range(lat_range, "lat"):
            raise ValueError(template.format("latitude"))
        if not Validators.is_valid_range(lon_range, "lon"):
            raise ValueError(template.format("longitude"))

    @staticmethod
    def is_valid_year(yr: int) -> bool:
        """
        Tests that the given year falls between 1970..2014
        :param yr: int year to test
        :return: bool: True or False
        """
        return eco_constants.YEAR_MIN <= yr <= eco_constants.YEAR_MAX

    @staticmethod
    def is_valid_month(mo: int) -> bool:
        """
        Tests that the given month falls between 1..12
        :param mo: int month to test
        :return:  bool: True or False
        """
        return eco_constants.MONTH_MIN <= mo <= eco_constants.MONTH_MAX

    @staticmethod
    def is_valid_quarter(qtr: int) -> bool:
        """
        Tests that the given quarter falls between 1..4
        :param qtr: quarter to test
        :return:  bool: True or False
        """
        return eco_constants.QTR_MIN <= qtr <= eco_constants.QTR_MAX

    @staticmethod
    def is_valid_year_range(yr_range: Tuple[int, int]) -> bool:
        (yr_lo, yr_hi) = yr_range
        return yr_lo < yr_hi \
               and Validators.is_valid_year(yr_lo) \
               and Validators.is_valid_year(yr_hi)

    @staticmethod
    def is_valid_latitude(lat: float) -> bool:
        """
        True if given latitude is within acceptable range
        :param lat: latitude
        :return: boolean
        """
        boundaries = {"min": - eco_constants.LAT_MAX, "max": - eco_constants.LAT_MIN}
        return (boundaries["min"] <= lat) and (lat <= boundaries["max"])

    @staticmethod
    def is_valid_longitude(lon: float) -> bool:
        """
        True if given longitude is within acceptable range
        :param lon: longitude
        :return: boolean
        """
        boundaries = {"min": eco_constants.LON_MIN, "max": eco_constants.LON_MAX}
        return (boundaries["min"] <= lon) and (lon <= boundaries["max"])
