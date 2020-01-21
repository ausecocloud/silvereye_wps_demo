from silvereye_wps_demo.models.ecomeasure import EcoMeasure


class Rainfall(EcoMeasure):
    def __init__(self):
        EcoMeasure.__init__(
            self,
            'http://dapds00.nci.org.au/thredds/dodsC/rr9/eMAST_data/ANUClimate/ANUClimate_v1-0_rainfall_daily_0-01deg_1970-2014',
            'lwe_thickness_of_precipitation_amount',
            'Rainfall'
        )
