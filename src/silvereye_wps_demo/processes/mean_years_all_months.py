import csv
import datetime
from itertools import takewhile, repeat
import logging
import operator
import os

from silvereye_wps_demo.models.ecocomposer import EcoComposer

from pywps import Process
from pywps import ComplexInput, ComplexOutput, LiteralInput, Format, BoundingBoxInput
from pywps.validator.mode import MODE

data = ['rainfall', 'temp_max', 'temp_min', 'vapour_pressure', 'solar_radiation']


class MeanYearsAllMonths(Process):
    def __init__(self):
        inputs = [
            LiteralInput(
                'variables', 'Variables to extract',
                data_type='string', min_occurs=1, max_occurs=len(data),
                mode=MODE.SIMPLE, allowed_values=data
            ),
            LiteralInput(
                'year_min', 'Minimum year to process in range 1970:2014',
                data_type='integer', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=(1970, 2014)
            ),
            LiteralInput(
                'year_max', 'Maximum year to process in range 1970:2014',
                data_type='string', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=(1970, 2014)
            ),
            LiteralInput(
                'lat_min', 'Latitude minimum value to process in range -43.735:-9.005',
                data_type='integer', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=(-43.735, -9.005)
            ),
            LiteralInput(
                'lat_max', 'Latitude maximum value to process in range -43.735:-9.005',
                data_type='integer', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=(-43.735, -9.005)
            ),
            LiteralInput(
                'lon_min', 'Longitude minimum value to process in range 112.905:153.995',
                data_type='integer', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=(112.905, 153.995)
            ),
            LiteralInput(
                'lon_max', 'Longitude maximum value to process in range 112.905:153.995',
                data_type='integer', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=(112.905, 153.995)
            ),
            # BoundingBoxInput(
            #     'coords', 'Coordinates of the rectangular geometry to process',
            #     'EPSG:4326',
            #     abstract='Latitude in range -43.735:-9.005. Longitude in range 112.905:153.995',
            #     dimensions=2, min_occurs=1, max_occurs=1, mode=MODE.NONE
            # ),
        ]

        outputs = [
            ComplexOutput('output', 'Metadata',
                          as_reference=True,
                          supported_formats=[Format('text/csv')]),
        ]

        super(MeanYearsAllMonths, self).__init__(
            self._handler,
            identifier='mean_years_all_months',
            title='ANUClim means by months for range of years.',
            abstract='Computes mean for env vars at location and time from ANUClimate daily climate grids.',
            version='1',
            metadata=[],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True)

    def _handler(self, request, response):
        # log = logging.getLogger(__name__)

        yr_min = request.inputs['year_min']
        yr_max = request.inputs['year_max']
        lat_min = request.inputs['lat_min']
        lat_max = request.inputs['lat_max']
        lon_min = request.inputs['lon_min']
        lon_max = request.inputs['lon_max']
        out_csv = os.path.join(self.workdir, 'out.csv')
        variables = [v for v in request.inputs['variables']]

        worker = EcoComposer(variables)
        worker.process_years_all_months(out_csv,
                                        (yr_min, yr_max),
                                        (lat_min, lat_max),
                                        (lon_min, lon_max))
        response.outputs['output'].file = out_csv
        return response
