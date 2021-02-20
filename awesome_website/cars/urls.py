from django.conf.urls import include, url
from django.urls import path, re_path

from cars.views import add_car, get_user_cars, delete_car, edit_car, get_car_vin_details, get_car_services, add_service, edit_service, delete_service, move_service
#from cars.views_api import CarList, get_user_car_api, CarListPost, edit_car_api_2
from cars.views_api import get_user_cars_api, add_car_api, edit_car_api, get_car_vin_details_api, delete_car_api, add_service_api, get_car_services_api, edit_service_api, delete_service_api

app_name = 'cars'

urlpatterns = [

    #path("car_list_api", CarList.as_view(), name='car-list-api'),
    
    re_path(r"get_user_cars_api", get_user_cars_api),
    re_path(r"add_car_api", add_car_api),
    re_path(r"edit_car_api", edit_car_api),
    #re_path(r"get_car_vin_details_api/<int:car_id>", get_car_vin_details_api),
    path(r"get_car_vin_details_api/<int:car_id>", get_car_vin_details_api),
    path(r"delete_car_api/<int:car_id>", delete_car_api),
    re_path(r"add_service_api", add_service_api),
    path(r"get_car_services_api/<int:car_id>", get_car_services_api),
    re_path(r"edit_service_api", edit_service_api),
    path(r"delete_service_api/<int:service_id>", delete_service_api),
    
    url(r"get_user_cars", get_user_cars, name="get_user_cars"),
    url(r"add_car", add_car, name="add_car"),
    path(r"delete_car/<int:car_id>", delete_car, name="delete_car"),
    path("edit_car/<int:car_id>", edit_car, name="edit_car"),
    path("get_car_services/<int:car_id>", get_car_services, name="get_car_services"),
    path("get_car_vin_details/<int:car_id>", get_car_vin_details, name="get_car_vin_details"),    
    path("add_service/<int:car_id>", add_service, name="add_service"),
    path("add_service", add_service, name="add_service"),    
    path("edit_service/<int:service_id>", edit_service, name="edit_service"),
    path("move_service/<int:service_id>", move_service, name="move_service"),
    path("delete_service/<int:service_id>", delete_service, name="delete_service"),

    

]

# (?P<drink_name>\D+)
# (?P<drink_name>\D+)
# (?P<car_model>\w+|)
# (?P<car_model>\w{0,50})