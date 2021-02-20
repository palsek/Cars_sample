import logging
import datetime
import requests

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_GET
from rest_framework import serializers

from .facades.db_facades import CarFacade, ServiceFacade
from .facades.api_facades import NHTSAFacade

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def add_car(request):

    logger.info("  ".join([str(request.user), str(request)]))
                
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "cars/add_car.html")
        else:
            # jeśli nie przyjdzie lub przyjdzie puste
            car_brand = request.POST.get('car_brand', '')
            car_model = request.POST.get('car_model', '')
            car_year = request.POST.get('car_year', '')
            car_vin = request.POST.get('car_vin', '')

            car_brand = car_brand if car_brand is not '' else '-'
            car_model = car_model if car_model is not '' else '-'
            car_year = car_year if car_year is not '' else 0
            car_vin = car_vin if car_vin is not '' else None
            
            user_id = request.user.id
            
            result = CarFacade.add_new_car(user_id, car_brand, car_model, car_year, car_vin)
                
            return HttpResponseRedirect(reverse('cars:get_user_cars'))
    else:
        return HttpResponseRedirect('/dashboard')


@require_GET
def get_user_cars(request):

    print("views / get_user_cars")
    
    logger.info("  ".join([str(request.user), str(request)]))
    
    if request.user.is_authenticated:
        
        cars = CarFacade.get_cars_by_user_id(request.user.id)
        
        context = {
            "user_cars": cars
        }
        
        return render(request, 'cars/show_user_cars.html', context)
    else:
        return HttpResponseRedirect('/dashboard')


@require_http_methods(["GET", "POST"])
#def edit_car(request, car_id=None, car_brand=None, car_model=None, car_year=None):
def edit_car(request, car_id):
    
    logger.info("  ".join([str(request.user), str(request)]))

    if request.user.is_authenticated:
        if request.method == "GET":
                        
            car = CarFacade.get_car_by_id(car_id)

            if car:
                context = {
                    "car_id": car_id,
                    "car_brand": car.brand,
                    "car_model": car.model,
                    "car_year": car.year,
                    "car_vin": car.vin
                }
            # car does not exist in db
            else:
                cars = car_facade.get_cars_by_user_id(request.user.id)
        
                context = {
                    "error_message": "Car with provided id does not exist.",
                    "user_cars": cars
                }

                return render(request, 'cars/show_user_cars.html', context)

            return render(request, "cars/edit_car.html", context)
        else:
            car_brand = request.POST.get('car_brand', '')
            car_model = request.POST.get('car_model', '')
            car_year = request.POST.get('car_year', '')
            car_vin = request.POST.get('car_vin', '')

            car_brand = car_brand if car_brand is not '' else '-'
            car_model = car_model if car_model is not '' else '-'
            car_year = car_year if car_year is not '' else 0
            car_vin = car_vin if car_vin is not '' else None

            CarFacade.edit_car(car_id, car_brand, car_model, car_year, car_vin)

            return HttpResponseRedirect(reverse('cars:get_user_cars'))
    else:
        return HttpResponseRedirect('/dashboard')


@require_GET
def get_car_vin_details(request, car_id):
    
    logger.info("  ".join([str(request.user), str(request)]))

    car = CarFacade.get_car_by_id(car_id)

    if car and car.vin:
        car_info = NHTSAFacade.get_car_info_by_vin(car.vin)
        return HttpResponse(car_info["response_data"])

    else:
        return HttpResponse("No car in data base or car has no vin.")
    

@require_GET
def delete_car(request, car_id):

    logger.info("  ".join([str(request.user), str(request)]))

    if request.user.is_authenticated:
        deleted_car = CarFacade.delete_car_by_id(car_id)

        if deleted_car:
            return HttpResponseRedirect(reverse('cars:get_user_cars'))
        else:
            # narazie jest to samo ale powinno być coś innego, co da użytkownikowi jakąs informację o błędzie
            return HttpResponseRedirect(reverse('cars:get_user_cars'))
    else:
        return HttpResponseRedirect('/dashboard')


@require_http_methods(["GET", "POST"])
def add_service(request, car_id=None):

    logger.info("  ".join([str(request.user), str(request)]))
    
    if request.user.is_authenticated:
        if request.method == "GET":

            context = {
                "car_id": car_id
            }

            return render(request, "services/add_service.html", context)

        else:            
            service_place = request.POST.get('service_place', '')
            service_repair = request.POST.get('service_repair', '')
            service_cost = request.POST.get('service_cost', '')
            service_date = request.POST.get('service_date', '')

            ServiceFacade.add_new_service(car_id, service_place, service_repair, service_cost, service_date)

            return HttpResponseRedirect(reverse('cars:get_car_services', kwargs={"car_id": car_id}))

    else:
        return HttpResponseRedirect('/dashboard')


@require_GET
def get_car_services(request, car_id):

    logger.info("  ".join([str(request.user), str(request)]))

    if request.user.is_authenticated:

        services = ServiceFacade.get_car_services(car_id)

        # True if services has at least one Service Object
        if services:
            car = services[0].car
        else:
            car = CarFacade.get_car_by_id(car_id)

        context = {
            "car": car,
            "car_services": services
        }
        
        return render(request, 'services/show_car_services.html', context)

    else:
        return HttpResponseRedirect('/dashboard')


@require_http_methods(["GET", "POST"])
def edit_service(request, service_id):

    logger.info("  ".join([str(request.user), str(request)]))

    if request.user.is_authenticated:

        if request.method == "GET":
            
            service = ServiceFacade.get_service_by_id(service_id)

            # change to str, because datetime.date is not supported by html
            service.date = str(service.date)
            context = {
                "service": service
            }

            return render(request, "services/edit_service.html", context)

        else:

            car_id = request.POST.get('car_id', '')
            #service_id = request.POST.get('service_id', '')
            service_place = request.POST.get('service_place', '')
            service_repair = request.POST.get('service_repair', '')
            service_cost = request.POST.get('service_cost', '')
            service_date = request.POST.get('service_date', '')
            
            ServiceFacade.edit_service(service_id, service_place, service_repair, service_cost, service_date, car_id)

            return HttpResponseRedirect(reverse('cars:get_car_services',  kwargs={"car_id": car_id}))

    else:
        return HttpResponseRedirect('/dashboard')


@require_http_methods(["GET", "POST"])
def move_service(request, service_id):

    logger.info("  ".join([str(request.user), str(request)]))

    if request.user.is_authenticated:

        if request.method == "GET":
            
            cars = CarFacade.get_cars_by_user_id(request.user.id)

            context = {
                "user_cars": cars
            }
        
            return render(request, 'services/choose_car_for_service.html', context)

        else:

            car_id_new = request.POST.get('car_id')

            ServiceFacade.edit_service(service_id, car_id=car_id_new)
            
            return HttpResponseRedirect(reverse('cars:get_car_services',  kwargs={"car_id": car_id_new}))

    else:
        return HttpResponseRedirect('/dashboard')




@require_GET
def delete_service(request, service_id):

    logger.info("  ".join([str(request.user), str(request)]))

    if request.user.is_authenticated:

        service = ServiceFacade.get_service_by_id(service_id)

        deletetion = ServiceFacade.delete_service_by_id(service_id)

        if deletetion:
            # narazie jest to samo ale powinno być coś innego, co da użytkownikowi jakąs informację o błędzie
            return HttpResponseRedirect(reverse('cars:get_car_services',  kwargs={"car_id": service.car.id}))
        else:
            return HttpResponseRedirect(reverse('cars:get_car_services',  kwargs={"car_id": service.car.id}))

    else:
        return HttpResponseRedirect('/dashboard')


