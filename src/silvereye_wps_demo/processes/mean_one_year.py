import csv
import datetime
from itertools import takewhile, repeat
import logging
import operator
import os

import numpy as np

from silvereye_wps_demo.models.ecocomposer import EcoComposer

from pywps import Process
from pywps import ComplexInput, ComplexOutput, LiteralInput, Format, BoundingBoxInput
from pywps.validator.mode import MODE

data = ['rainfall', 'temp_max', 'temp_min', 'vapour_pressure', 'solar_radiation']


class MeanOneYear(Process):
    def __init__(self):
        inputs = [
            LiteralInput(
                'variables', 'Variables to extract',
                data_type='string', min_occurs=1, max_occurs=len(data),
                mode=MODE.SIMPLE, allowed_values=data
            ),
            LiteralInput(
                'year', 'Year to process, in range 1970:2014',
                data_type='integer', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=[[1970, 2014]]
            ),
            LiteralInput(
                'lat_min', 'Latitude minimum value to process in range -43.735:-9.005',
                data_type='float', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=[[-43.735, -9.005]]
            ),
            LiteralInput(
                'lat_max', 'Latitude maximum value to process in range -43.735:-9.005',
                data_type='float', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=[[-43.735, -9.005]]
            ),
            LiteralInput(
                'lon_min', 'Longitude minimum value to process in range 112.905:153.995',
                data_type='float', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=[[112.905, 153.995]]
            ),
            LiteralInput(
                'lon_max', 'Longitude maximum value to process in range 112.905:153.995',
                data_type='float', min_occurs=1, max_occurs=1,
                mode=MODE.SIMPLE, allowed_values=[[112.905, 153.995]]
            ),
        ]

        outputs = [
            ComplexOutput('output', 'Metadata',
                          as_reference=True,
                          supported_formats=[Format('text/csv')]),
        ]

        super(MeanOneYear, self).__init__(
            self._handler,
            identifier='mean_one_year',
            title='ANUClim yearly means for one year.',
            abstract="Computes yearly averages (mean) for env vars at location and time from ANUClimate daily climate grids.",
            version='1',
            metadata=[],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True)

    def _handler(self, request, response):
        # log = logging.getLogger(__name__)

        yr = request.inputs['year'][0].data
        lat_min = request.inputs['lat_min'][0].data
        lat_max = request.inputs['lat_max'][0].data
        lon_min = request.inputs['lon_min'][0].data
        lon_max = request.inputs['lon_max'][0].data
        out_csv = os.path.join(self.workdir, 'out.csv')
        variables = [v.data for v in request.inputs['variables']]

        worker = EcoComposer(variables)
        worker.process_one_year(out_csv,
                                yr,
                                (lat_min, lat_max),
                                (lon_min, lon_max))

        response.outputs['output'].file = out_csv
        return response
