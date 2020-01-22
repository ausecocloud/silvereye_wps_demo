from pyramid.view import view_config
from pyramid.wsgi import wsgiapp2

from pywps import Service

from silvereye_wps_demo.processes.mean_one_year_all_months import MeanOneYearAllMonths
from silvereye_wps_demo.processes.mean_one_year_all_quarters import MeanOneYearAllQuarters
from silvereye_wps_demo.processes.mean_one_year_month_range import MeanOneYearMonthRange
from silvereye_wps_demo.processes.mean_one_year_one_month import MeanOneYearOneMonth
from silvereye_wps_demo.processes.mean_one_year_one_quarter import MeanOneYearOneQuarter
from silvereye_wps_demo.processes.mean_years_all_months import MeanYearsAllMonths
from silvereye_wps_demo.processes.mean_years_all_quarters import MeanYearsAllQuarters
from silvereye_wps_demo.processes.mean_years_one_month import MeanYearsOneMonth
from silvereye_wps_demo.processes.mean_years_one_quarter import MeanYearsOneQuarter
from silvereye_wps_demo.processes.mean_years import MeanYears
from silvereye_wps_demo.processes.mean_one_year import MeanOneYear

processes = [
    MeanOneYearAllMonths(),
    MeanOneYearAllQuarters(),
    MeanOneYearMonthRange(),
    MeanOneYearOneMonth(),
    MeanOneYearOneQuarter(),
    MeanYearsAllMonths(),
    MeanYearsAllQuarters(),
    MeanYearsOneMonth(),
    MeanYearsOneQuarter(),
    MeanOneYear(),
    MeanYears(),
]

service = Service(processes, ['/etc/silvereye/pywps.cfg'])


@view_config(route_name='wps')
@wsgiapp2
def wps_app(environ, start_response):
    response = service(environ, start_response)
    return response
