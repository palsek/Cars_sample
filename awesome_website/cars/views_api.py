'''
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
'''

import logging
import pdb

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .facades.db_facades import CarFacade, ServiceFacade
from .facades.api_facades import NHTSAFacade
from .serializers import CarSerializer, ServiceSerializer


# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


@api_view(['POST'])
def add_car_api(request):

    logger.info("  ".join([str(request.user), str(request)]))

    serializer = CarSerializer(request.data)

    if serializer.is_valid:
        user_id = request.user.id
        brand = serializer.data.get("brand", None)
        model = serializer.data.get("model", None)
        year = serializer.data.get("year", None)
        vin = serializer.data.get("vin", None)

        # There is possibility to save data using serializer, but I prefer use facade.
        car_id = CarFacade.add_new_car(user_id=user_id, brand=brand, model=model, year=year, vin=vin)

        serializer.data["car_id"] = car_id

    if car_id:
        return Response({"result": "New car has been added", "car_id": car_id}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
#@authentication_classes([])
#@permission_classes([])
def get_user_cars_api(request):

    logger.info("  ".join([str(request.user), str(request)]))

    user = request.user
    cars = CarFacade.get_cars_by_user_id(user.id)

    car = cars[0]

    serializer = CarSerializer(cars, many=True)

    if serializer.is_valid:
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_car_api(request):

    logger.info("  ".join([str(request.user), str(request)]))
    
    serializer = CarSerializer(request.data)

    if serializer.is_valid:

        user_id = request.user.id
        car_id = request.data.get("car_id", None)
        brand = serializer.data.get("brand", None)
        model = serializer.data.get("model", None)
        year = serializer.data.get("year", None)
        vin = serializer.data.get("vin", None)

        # checking if car belongs to the user
        if not CarFacade.check_car_user(car_id, user_id):
            return Response({"result": "Car not match to user."}, status=status.HTTP_400_BAD_REQUEST)

        edit_result = CarFacade.edit_car(car_id=car_id, car_brand=brand, car_model=model, car_year=year, car_vin=vin)

        if edit_result:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"result": "Car probably not found in db."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_car_vin_details_api(request, car_id):
    
    logger.info("  ".join([str(request.user), str(request)]))


    # checking if car belongs to the user
    if not CarFacade.check_car_user(car_id, request.user.id):
        return Response({"result": "Car not match to user."}, status=status.HTTP_400_BAD_REQUEST)

    car = CarFacade.get_car_by_id(car_id)

    if car and car.vin:
        car_info = NHTSAFacade.get_car_info_by_vin(car.vin)
        return Response(car_info)
    else:
        return Response({"result": "No car in data base or car has no vin."})


@api_view(['DELETE'])
def delete_car_api(request, car_id):

    logger.info("  ".join([str(request.user), str(request)]))

    # checking if car belongs to the user
    if not CarFacade.check_car_user(car_id, request.user.id):
        return Response({"result": "Car not match to user."}, status=status.HTTP_404_NOT_FOUND)

    removal_result = CarFacade.delete_car_by_id(car_id)
    
    if removal_result:
        return Response({"result": "Car has been deleted."}, status=status.HTTP_200_OK)
    else:
        return Response({"result": "Nothing has been deleted, because car did not exist."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_service_api(request):

    logger.info("  ".join([str(request.user), str(request)]))

    serializer = ServiceSerializer(request.data)

    if serializer.is_valid:

        user_id = request.user.id
        car_id = serializer.data.get("car_id", None) 
        place = serializer.data.get("place", None)
        repair = serializer.data.get("repair", None)
        cost = serializer.data.get("cost", None)
        date = serializer.data.get("date", None)

        # checking if car belongs to the user
        if not CarFacade.check_car_user(car_id, user_id):
            return Response({"result": "Car not match to user."}, status=status.HTTP_404_NOT_FOUND)

        if car_id:
            service_id = ServiceFacade.add_new_service(car_id=car_id, place=place, repair=repair, cost=cost, date=date)
            if service_id:            
                return Response({"service_id": service_id}, status=status.HTTP_201_CREATED)
            else:
                return Response({"result": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)    
        else:
            return Response({"result": "Request has to contain car_id element."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_car_services_api(request, car_id):

    logger.info("  ".join([str(request.user), str(request)]))

    # checking if car belongs to the user
    if not CarFacade.check_car_user(car_id, request.user.id):
        return Response({"result": "Car not match to user."}, status=status.HTTP_404_NOT_FOUND)

    services = ServiceFacade.get_car_services(car_id)

    serializer = ServiceSerializer(services, many=True)

    if serializer.is_valid:
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_service_api(request):

    logger.info("  ".join([str(request.user), str(request)]))

    serializer = ServiceSerializer(request.data)

    if serializer.is_valid:
        user_id = request.user.id
        service_id = request.data.get("service_id", None)
        place = serializer.data.get("place", None)
        repair = serializer.data.get("repair", None)
        cost = serializer.data.get("cost", None)
        date = serializer.data.get("date", None)

        # checking if service belongs to the user
        if not service_id or not ServiceFacade.check_service_user(service_id, user_id):
            return Response({"result": "Service not match to user. service_id is obligatory in request."}, status=status.HTTP_404_NOT_FOUND)

        edit_result = ServiceFacade.edit_service(service_id=service_id, service_place=place, service_repair=repair, service_cost=cost, service_date=date)

        if edit_result:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"result": "Service probably not found in db."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_service_api(request, service_id):
    
    logger.info("  ".join([str(request.user), str(request)]))

    # checking if service belongs to the user
    if not ServiceFacade.check_service_user(service_id, request.user.id):
        return Response({"result": "Service not match to user."}, status=status.HTTP_404_NOT_FOUND)

    removal_result = ServiceFacade.delete_service_by_id(service_id=service_id)

    if removal_result:
        return Response({"result": "Service has been deleted."}, status=status.HTTP_200_OK)
    else:
        return Response({"result": "Nothing has been deleted, because service did not exist."}, status=status.HTTP_404_NOT_FOUND)
