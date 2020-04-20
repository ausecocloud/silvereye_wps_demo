# README.md

## Introduction

This is a prototype for the "SilverEye" project.
It implements core functions that calculate the basic functionality.
This program performs the following tasks:
* It reads the ANU Climate variables (temp_max, temp_min, rainfall, solar_radiation, vapour_pressure) 
from remote databases, via PyDap.
* It works on specified latitude and longitude rectangular regions (within Australia), 
* It produces monthly, quarterly, yearly average time reductions, as follows: 
    * Monthly Averages (Means)
        * Means for one year, one month
        * Means for one year, all months
        * Means for one year, and a range of months
        * Means for a range of years, all months
        * Means for a range of years, one month of each year
        * Means for year-month to year-month interval
    * Quarterly Averages (Means)
        * Means for one year, one quarter
        * Means for one year, all quarters
        * Means for a range of years, all quarters
        * Means for a range of years, one quarter of each year
    * Yearly Averages (Means)
        * Means for one year
        * Means for a range of years
    * Reports are generated in CSV file format.
* The WPS standard is used as an interface to the core functions, each of which is implemented as a WPS process.
* These core functions are wrapped into a web application using the Pyramid framework.
* The whole application is additionally wrapped into a docker container. 

## Technology Dependencies

The project currently relies on the following technologies:
* Python 3.7.*
* NumPy: NDArrays with mean calculations
* PyDap: for connecting to remote ANU Climate files
* Requests: required by PyDap
* PyWPS: Python's implementation of the WPS standard (for processes, inputs and outputs)   
* Pyramid: Python framework for web applications
* Docker: for wrapping the webapp into a stand-alone container
    
## Preparation

Requires Python 3.7.x.

For GitHub: 
* Do a Fork and a Pull request. 
* Clone the forked project.

Prepare and activate a virtual environment:

```shell
cd silvereye_wps_demo
python -m venv env
source env/bin/activate
```

Install dependencies and set up project:
```shell 
pip install -e .
python setup.py develop
```

## To Execute 

To run the application stand-alone (for development):
```shell
cd silvereye_wps_demo
env/bin/pserve development.ini --reload
```


To run the application as a docker container:

```shell
docker-compose build
docker-compose up

```

## To Invoke

The following processes have been implemented:
* mean_one_year_all_months
* mean_one_year_all_quarters
* mean_one_year_month_range
* mean_one_year_one_month
* mean_one_year_one_quarter
* mean_years_all_months
* mean_years_all_quarters
* mean_years_one_month
* mean_years_one_quarter
* mean_one_year
* mean_years
* mean_year_month_range

Inputs depend on each process, and include:
* year (int), or range of years, with values between 1970 and 2014.
* month (int), or range of months, with values between 1 and 12.
* year-month to year-month, within the ranges specified above.
* quarter (int), with values between 1 and 4.
* latitude pair (floats) (min, max), with values in the range -43.735:-9.005
* longitude pair (floats) (min, max), with values in the range 112.905:153.995

For specific inputs to each process, check the files under:
```shell
src/silvereye_wps_demo/processes/mean_*.py
```
### Sample Invocation:

Invoke it with Insomnia or with Postman.

Endpoint: `POST http://0.0.0.0:6543/wps`

Headers:
* Content-Type: "application/xml"
* Accept: "application/xml"

Payload (Body):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<wps:Execute 
	service="WPS"
	version="1.0.0"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.opengis.net/wps/1.0.0"
	xmlns:wps="http://www.opengis.net/wps/1.0.0"
	xmlns:ows="http://www.opengis.net/ows/1.1"
	xsi:schemaLocation="http://www.opengis.net/wps/1.0.0  http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">
	<ows:Identifier>mean_years_one_quarter</ows:Identifier>
	<wps:DataInputs>
		<wps:Input>
			<ows:Identifier>variables</ows:Identifier>
			<wps:Data>
				<wps:LiteralData>rainfall</wps:LiteralData>
			</wps:Data>
		</wps:Input>
		<wps:Input>
			<ows:Identifier>year_min</ows:Identifier>
			<wps:Data>
				<wps:LiteralData>1990</wps:LiteralData>
			</wps:Data>
		</wps:Input>
		<wps:Input>
			<ows:Identifier>year_max</ows:Identifier>
			<wps:Data>
				<wps:LiteralData>1991</wps:LiteralData>
			</wps:Data>
		</wps:Input>
		<wps:Input>
			<ows:Identifier>quarter</ows:Identifier>
			<wps:Data>
				<wps:LiteralData>3</wps:LiteralData>
			</wps:Data>
		</wps:Input>
		<wps:Input>
			<ows:Identifier>lat_min</ows:Identifier>
			<wps:Data>
				<wps:LiteralData>-28.12</wps:LiteralData>
			</wps:Data>
		</wps:Input>
		<wps:Input>
			<ows:Identifier>lat_max</ows:Identifier>
			<wps:Data>
				<wps:LiteralData>-27.94</wps:LiteralData>
			</wps:Data>
		</wps:Input>
		<wps:Input>
			<ows:Identifier>lon_min</ows:Identifier>
			<wps:Data>
				<wps:LiteralData>152.85</wps:LiteralData>
			</wps:Data>
		</wps:Input>
		<wps:Input>
			<ows:Identifier>lon_max</ows:Identifier>
			<wps:Data>
				<wps:LiteralData>153.25</wps:LiteralData>
			</wps:Data>
		</wps:Input>
	</wps:DataInputs>
	<wps:ResponseForm>
		<wps:ResponseDocument lineage="true" 
		        storeExecuteResponse="true" status="true">
			<wps:Output asReference="false">
				<ows:Identifier>result</ows:Identifier>
			</wps:Output>
		</wps:ResponseDocument>
	</wps:ResponseForm>
</wps:Execute>
```

## Output

If running from a docker container, the output is written to the following folders:
* `volumes/wps_workdir/outputs` contains out.csv files
* `volumes/wps_log/pywps-logs.sqlite3` contains a sqlite3 database with the logs.

## Troubleshooting 

If the above installation of dependencies fails, 
or misses something, try the following:

Install dependencies:
```shell
pip install -e .
```

Install dependencies for development:
```shell
pip install -r ".[dev]"
```
