import logging

from cars.models import Car, Service

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

class CarFacade():

    @classmethod
    def add_new_car(cls, user_id, brand=None, model=None, year=None, vin=None):
        """Add new car to database\n
        return car id
        """

        logger.info("add_new_car / {}".format(locals()))

        car = Car(brand=brand, model=model, year=year, vin=vin, user_id=user_id)
        car.save()

        return car.id


    @classmethod
    def get_car_by_id(cls, car_id):
        """
        :param car_id int: id of car\n
        :return Car object or None: Car object if find car in db otherwise None
        """

        logger.info("get_car_by_id / {}".format(locals()))

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist as car_not_exists:
            logger.warning(car_not_exists)
            return None
        else:
            return car


    @classmethod
    def get_cars_by_user_id(cls, user_id):
        """
        :param user_id int: id of user\n
        :return QuerySet: Query set of user cars
        """

        logger.info("get_cars_by_user_id / {}".format(locals()))
        
        cars = Car.objects.filter(user_id=user_id).order_by('id')
        return cars


    @classmethod
    def edit_car(cls, car_id, car_brand=None, car_model=None, car_year=None, car_vin=None):

        logger.info("edit_car / {}".format(locals()))
        try:
            car = Car.objects.get(id=car_id)    
        except Car.DoesNotExist:
            return None
        
        if car_brand:
            car.brand = car_brand
        if car_model:
            car.model = car_model
        if car_year:
            car.year = car_year
        if car_vin:
            car.vin = car_vin

        car.save()
        return car.id
    
    @classmethod
    def delete_car_by_id(cls, car_id):
        """
        :param car_id int: service id\n
        :return tuple: number of objects deleted and a dictionary with the number of deletions per object type\n
        if car not exists return None
        """

        logger.info("delete_car_by_id / {}".format(locals()))
        
        try:            
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist as car_not_exist:
            logger.warning(car_not_exist)
            return None
        else:
            return car.delete()


    @classmethod
    def check_car_user(cls, car_id, user_id):
        """
        Check if user is the owner of the car
        :param car_id int: car id\n
        :param user_id int: user id\n
        :return True if car belong to the user, otherwise False
        """

        logger.info("check_car_user / {}".format(locals()))

        try:
            Car.objects.get(id=car_id, user_id=user_id)
        except Car.DoesNotExist as car_not_exist:
            logger.warning(car_not_exist)
            return False
        else:
            return True



class ServiceFacade():

    @classmethod
    def add_new_service(cls, car_id, place=None, repair=None, cost=None, date=None):
        """
        :param place str: service place\n
        :param repair str service repair\n
        :param cost int/decimal: cost service id\n
        :param date str: date of service id\n
        :param car_id int: car id\n        
        :return int: service id
        """

        logger.info("add_new_service / {}".format(locals()))

        date = date if date != '' else None
        cost = cost if cost != '' else None
        
        service = Service(place=place, repair=repair, cost=cost, date=date, car_id=car_id)

        try:
            service.save()
        except Exception as error:
            logger.error(error)
        else:
            return service.id


    @classmethod
    def get_service_by_id(cls, service_id):
        """
        :param service_id int: service id\n        
        :return Service object:
        """

        logger.info("get_service_by_id / {}".format(locals()))

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist as service_not_exists:
            logger.warning(service_not_exists)
            return None
        else:
            return service
    

    @classmethod
    def get_car_services(cls, car_id):
        """
        :param car_id int: car id\n        
        :return QuerySet: Query Set of services
        """

        logger.info("get_car_services / {}".format(locals()))

        services = Service.objects.filter(car_id=car_id)
        
        return services if len(services) > 0 else None

    
    @classmethod
    def edit_service(cls, service_id, service_place=None, service_repair=None, service_cost=None, service_date=None, car_id=None):
        """
        :param service_id int: service id\n
        :param service_place str: service place\n
        :param service_repair str service repair\n
        :param service_cost int/decimal: cost service id\n
        :param service_date str: date of service id\n
        :param car_id int: car id\n        
        :return int: service id if Passed or None if Failed
        """

        logger.info("edit_service / {}".format(locals()))

        try:
            service = Service.objects.get(id=service_id)
        except:
            #import pdb
            #pdb.set_trace()
            return None

        if service_place:
            service.place = service_place

        if service_repair:
            service.repair = service_repair

        if service_cost:
            service.cost = service_cost

        if service_date:
            service.date = service_date

        if car_id:
            car = CarFacade.get_car_by_id(car_id)
            service.car = car

        service.save()
        return service.id
        
    
    @classmethod
    def delete_service_by_id(cls, service_id):
        """
        :param service_id int: service id\n
        :return tuple: number of objects deleted and a dictionary with the number of deletions per object type
        if service not exists return None
        """

        logger.info("delete_service_by_id / {}".format(locals()))

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist as service_not_exists:
            logger.warning(service_not_exists)
            return None
        else:
            return service.delete()

    
    @classmethod
    def check_service_user(cls, service_id, user_id):
        """
        Check if user is the owner of the service
        :param service_id int: service id\n
        :param user_id int: user id\n
        :return True if car/service belong to the user, otherwise False
        """

        logger.info("check_service_user / {}".format(locals()))

        try:
            service = Service.objects.get(id=service_id)
            if service.car.user_id == user_id:
                return True
        except Service.DoesNotExist as service_not_exist:
            logger.warning(service_not_exist)
            return False
