from silvereye_wps_demo.models.ecomeasure import EcoMeasure


class VapourPressure(EcoMeasure):
    """Vapour Pressure"""

    def __init__(self):
        EcoMeasure.__init__(
            self,
            'http://dapds00.nci.org.au/thredds/dodsC/rr9/eMAST_data/ANUClimate/ANUClimate_v1-1_vapour-pressure_daily_0-01deg_1970-2014',
            'vapour_pressure',
            'VapourPressure'
        )
