
# README.md


## Preparation

Requires Python 3.7.x installed on your computer.

Clone this project:

```shell
git clone https://gitlab.rcs.griffith.edu.au/d.guillen/silvereye-wps-demo.git
```

Prepare and activate a virtual environment:

```shell
cd silvereye_wps_demo
python -m venv env
source env/bin/activate
```

Install dependencies:
```shell 
pip install -r requirements.txt
```

## To Execute 

```shell
env/bin/pserve development.ini --reload

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

Inputs to the processes are:
* year (int), or range of years, in the range 1970:2014
* month (int), or range of months, in the range 1:12
* year-month to year-month, within the ranges specified above
* quarter (int) in the range 1:4
* latitude pair (floats) (min, max) in the range -43.735:-9.005
* longitude pair (floats) (min, max) in the range 112.905:153.995

For specific inputs to each process, check the files under:
```shell
src/silvereye_wps_demo/processes/mean_*.py
```
### Sample Invocation:

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
	xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 
	    http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">
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
