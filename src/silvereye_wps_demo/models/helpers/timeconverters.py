import datetime
import calendar
from typing import Tuple


class TimeConverters(object):

    @staticmethod
    def ts2iso(ts: float) -> str:
        """
        convert date from timestamp to isoformat
        :param ts: date in timestamp format
        :return: date in iso format '1970-12-31'
        """
        return datetime.date.fromtimestamp(ts).isoformat()

    @staticmethod
    def iso2ts(iso: str = '1970-01-01') -> float:
        """
        Convert date from isoformat to timestamp.
        Example: f('1970-01-01') -> 0.0
        :param iso: date in iso format
        :return: date in timestamp format
        """
        offset = 10 * 60 * 60   # correction for Brisbane AEST
        return datetime.datetime.fromisoformat(iso).timestamp() + offset

    @staticmethod
    def ym2trange(yr: int, mo: int) -> Tuple:
        """
        Converts year month to tuple with lo and hi date values in iso format.
        Compensates February last day for leap years.
        Example: f(2000, 6) -> ("2000-06-01", "2000-06-30")
        :param yr: int, year in range 1970..2014
        :param mo: int, month in range 1..12
        :return: Tuple (date_lo_iso, date_hi_iso)
        """
        days_in_month = [
            31, 28, 31, 30, 31, 30,
            31, 31, 30, 31, 30, 31]
        if calendar.isleap(yr):
            days_in_month[1] = 29
        return ("{:04d}-{:02d}-01".format(yr, mo),
                "{:04d}-{:02d}-{:02d}".format(yr, mo, days_in_month[mo - 1]))

    @staticmethod
    def y2trange(yr: int) -> Tuple:
        """
        Converts year to tuple with lo and hi date values in iso format.
        Example: f(2000) -> ("2000-01-01", "2000-12-31")
        :param yr: int, year in range 1970..2014
        :return: Tuple (date_lo_iso, date_hi_iso)
        """
        return ("{:04d}-01-01".format(yr), "{:04d}-12-31".format(yr))

    @staticmethod
    def ym2iso(yr: int, mo: int) -> str:
        """
        Converts year, month numbers to iso format.
        :param yr: year in range 1970..2014
        :param mo: month in range 1..12
        :return: str in "YYYY-MM" format. Example: f(1990, 6) -> "1990-06"
        """
        return "{:04d}-{:02d}".format(yr, mo)

    @staticmethod
    def yq2iso(yr: int, qtr: int) -> str:
        """
        Converts year, quarter numbers into iso format.
        :param yr: year in range 1970..2014
        :param qtr: quarter in range 1..4
        :return: str in "YYYY-MM" format. Example: f(1990, 3) -> "1990-q3"
        """
        return "{:04d}-q{}".format(yr, qtr)

    @staticmethod
    def yq2trange(yr: int, qtr: int) -> Tuple:
        """
        Converts year quarter to tuple with lo and hi date values in iso format.
        Example: f(2000, 2) -> ("2000-04-01", "2000-06-30")
        :param yr: year in range 1970..2014
        :param qtr: quarter in range 1..4
        :return: Tuple (date_lo_iso, date_hi_iso)
        """
        quarters = {
            1: ("01-01", "03-31"),
            2: ("04-01", "06-30"),
            3: ("07-01", "09-30"),
            4: ("10-01", "12-31")
        }
        (qtr_lo, qtr_hi) = quarters[qtr]
        return ("{:04d}-{}".format(yr, qtr_lo),
                "{:04d}-{}".format(yr, qtr_hi))

