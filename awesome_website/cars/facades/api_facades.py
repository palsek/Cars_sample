import requests
import json
import logging

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

#NHTSA - means United States Department of Transportation
class NHTSAFacade():

    BASE_URL = r"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvalues/"

    @classmethod    
    def get_car_info_by_vin(cls, vin):

        logger.info("get_car_info_by_vin / {}".format(locals()))

        car_service_url = "{}{}{}".format(cls.BASE_URL, vin, "?format=json")

        logger.info("car_service_ulr: {}".format(car_service_url))

        try:
            # call external service
            response = requests.get(car_service_url)
        except requests.exceptions.Timeout:
            return {
                "error_detail": "Timeout exception raised during external service call",
                "response_data": None
            }
        except requests.exceptions.RequestException:
            return {
                "error_detail": "Unknown exception raised during external service call",
                "response_data": None
            }

        if response.status_code == 200:
            return {
                "error_detail": None,
                #"response_data": json.loads(response.content)
                "response_data": response.content
            }
        else:
            return {
                "error_detail": None,
                "response_data": "Error during call external service. Response code = {}".format(response.status_code)
            }

        
        
