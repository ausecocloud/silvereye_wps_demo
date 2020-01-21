from pyramid.view import view_config
from pyramid.wsgi import wsgiapp2

from pywps import Service

# from silvereye_wps_demo.processes.anuclim_daily_extract import ANUClimDailyExtract
# from silvereye_wps_demo.processes.anuclim_daily_extract_netcdf4 import ANUClimDailyExtractNetCDF4
# from silvereye_wps_demo.processes.spatial_subset_geotiff import SpatialSubsetGeotiff
# from silvereye_wps_demo.processes.spatial_subset_netcdf import SpatialSubsetNetcdf
# from silvereye_wps_demo.processes.exploratory_data_box import ExploratoryDataBox
# from silvereye_wps_demo.processes.exploratory_data_histogram import ExploratoryDataHistogram
# from silvereye_wps_demo.processes.exploratory_data_density import ExploratoryDataDensity
# from silvereye_wps_demo.processes.exploratory_data_correlation import ExploratoryDataCorrelation

from silvereye_wps_demo.processes.mean_one_year_all_months import MeanOneYearAllMonths
from silvereye_wps_demo.processes.mean_one_year_all_quarters import MeanOneYearAllQuarters
from silvereye_wps_demo.processes.mean_one_year_one_month import MeanOneYearOneMonth
from silvereye_wps_demo.processes.mean_one_year_one_quarter import MeanOneYearOneQuarter
from silvereye_wps_demo.processes.mean_years_all_months import MeanYearsAllMonths
from silvereye_wps_demo.processes.mean_years_all_quarters import MeanYearsAllQuarters
from silvereye_wps_demo.processes.mean_years_one_month import MeanYearsOneMonth
from silvereye_wps_demo.processes.mean_years_one_quarter import MeanYearsOneQuarter



processes = [
    # ANUClimDailyExtract(),
    # ANUClimDailyExtractNetCDF4(),
    # SpatialSubsetGeotiff(),
    # SpatialSubsetNetcdf(),
    # ExploratoryDataBox(),
    # ExploratoryDataHistogram(),
    # ExploratoryDataDensity(),
    # ExploratoryDataCorrelation(),

    MeanOneYearAllMonths(),
    MeanOneYearAllQuarters(),
    MeanOneYearOneMonth(),
    MeanOneYearOneQuarter(),
    MeanYearsAllMonths(),
    MeanYearsAllQuarters(),
    MeanYearsOneMonth(),
    MeanYearsOneQuarter()
]


service = Service(processes, ['/etc/silvereye/pywps.cfg'])


@view_config(route_name='wps')
@wsgiapp2
def wps_app(environ, start_response):
    response = service(environ, start_response)
    return response
