import pdb
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Car, Service
from .facades.db_facades import CarFacade, ServiceFacade
from users.forms import CustomUserCreationForm


def add_few_cars_to_db():
    print("add_few_cars_to_db")

    new_car_1 = Car(brand="opel", model="mokka", year=2018, user_id=1)
    new_car_2 = Car(brand="ford", model="fiesta", year=2013, user_id=1)
    new_car_3 = Car(brand="audi", model="a3", year=2008, user_id=1)
    new_car_4 = Car(brand="ford", model="mondeo", year=2002, user_id=2)
    new_car_5 = Car(brand="kia", model="sorento", year=2002, user_id=3)

    new_car_1.save()
    new_car_2.save()
    new_car_3.save()
    new_car_4.save()
    new_car_5.save()
        
    car_ids = [new_car_1.id, new_car_2.id, new_car_3.id, new_car_4.id, new_car_5.id]
    
    return car_ids


def add_few_cars_and_services_to_db():
    print(add_few_cars_and_services_to_db)

    car_ids = add_few_cars_to_db()

    # dict when key is car id and value is list of services ids
    car_service_ids = {}
    
    for i, car_id in enumerate(car_ids):

        car_db = Car.objects.get(id=car_id)

        #import pdb
        #pdb.set_trace()

        # the last car will not have service
        if i < len(car_ids)-1:

            service_1 = Service(place="place service {} for car {}".format(str(i+1), car_id), \
            repair="repair service {} for car {}".format(str(i+1), car_id), cost=110.50,  \
            date="2019-05-12", car=car_db)

            service_2 = Service(place="place service {} for car {}".format(str(i+2), car_id), \
            repair="repair service {} for car {}".format(str(i+2), car_id), cost=110.50, \
            date="2019-05-12", car=car_db)
            
            service_3 = Service(place="place service {} for car {}".format(str(i+3), car_id), \
            repair="repair service {} for car {}".format(str(i+3), car_id), cost=110.50, \
            date="2019-05-12", car=car_db)

            service_1.save()
            service_2.save()
            service_3.save()

            service_ids = [service_1.id, service_2.id, service_3.id]

            car_service_ids[car_id] = service_ids

        #pdb.set_trace()

        #print("---------------------------------------------------------------------start")
        #print(i)
        #print(car_id)
        #print(len(Service.objects.filter()))
        #print("---------------------------------------------------------------------stop")

    return car_service_ids


class CarModelTests(TestCase):
   
    
    def test_add_new_car(self):

        new_car = Car(brand="opel", model="mokka", year=2018, user_id=1)
        
        CarFacade.add_new_car(new_car.user_id, new_car.brand, new_car.model, new_car.year)

        db_car = Car.objects.get(pk=1)
        
        self.assertEqual(new_car.brand, db_car.brand)
        self.assertEqual(new_car.model, db_car.model)
        self.assertEqual(new_car.year, db_car.year)
        self.assertEqual(new_car.user_id, db_car.user_id)


    def test_get_car_by_id(self):
        add_few_cars_to_db()
        
        cars = CarFacade.get_cars_by_user_id(1)
        car = CarFacade.get_car_by_id(cars[0].id)
        
        self.assertEqual(cars[0].id, car.id)

    def test_get_car_by_id_if_no_car(self):
        
        car = CarFacade.get_car_by_id(999)

        self.assertIs(None, car)

    
    def test_get_cars_by_user_id(self):
        
        add_few_cars_to_db()
        
        cars = CarFacade.get_cars_by_user_id(1)

        self.assertEqual(3, len(cars))
        self.assertEqual("opel", cars[0].brand)
        self.assertEqual(1, cars[0].user_id)
        self.assertEqual([1,1,1], [car.user_id for car in cars])

    
    def test_edit_car(self):

        add_few_cars_to_db()
        
        edited_car = Car(brand="kiszka", model="piszka", year=200, user_id=3)
        
        check_car = Car.objects.get(brand="kia", model="sorento", year=2002, user_id=3)        
        
        CarFacade.edit_car(check_car.id, edited_car.brand, edited_car.model, edited_car.year)

        modified_car = Car.objects.get(id=check_car.id)

        self.assertEqual(edited_car.brand, modified_car.brand)
        self.assertEqual(edited_car.model, modified_car.model)
        self.assertEqual(edited_car.year, modified_car.year)
        self.assertEqual(edited_car.user_id, modified_car.user_id)


    def test_edit_car__car_not_exists(self):
        add_few_cars_to_db()

        # get last car from db
        car = Car.objects.last()

        edit_result = CarFacade.edit_car(car.id+1, "b", "m", 2000)

        self.assertEqual(None, edit_result)



    def test_delete_car_by_id(self):
        add_few_cars_to_db()
        
        check_car = Car.objects.get(brand="kia", model="sorento", year=2002, user_id=3)

        delete_result = CarFacade.delete_car_by_id(check_car.id)
        
        self.assertNotEqual(None, delete_result)

        with self.assertRaises(Car.DoesNotExist):
            del_car = Car.objects.get(id=check_car.id)


    def test_delete_car_by_id__id_not_exists(self):

        delete_result = CarFacade.delete_car_by_id(999)

        self.assertEqual(None, delete_result)


    def test_check_car_user(self):
        car_ids = add_few_cars_to_db()
        result = CarFacade.check_car_user(car_ids[0], 1)
        self.assertTrue(result)


    def test_check_car_user__negative(self):
        car_ids = add_few_cars_to_db()
        result = CarFacade.check_car_user(car_ids[0], 2)
        self.assertFalse(result)


class ServiceModelTests(TestCase):

    def test_add_new_service(self):
        
        add_few_cars_to_db()

        car = Car.objects.filter().first()
                
        ServiceFacade.add_new_service(car.id, "place value", "repair value", 12.50, "2020-06-23")
        
        service_db = Service.objects.get(car=car)

        self.assertEqual("place value", service_db.place)
        self.assertEqual("repair value", service_db.repair)
        self.assertEqual(12.50, service_db.cost)
        self.assertEqual( "2020-06-23", str(service_db.date))


    def test_add_new_service_2(self):
        
        add_few_cars_to_db()

        car = Car.objects.filter().first()
        
        ServiceFacade.add_new_service(car.id, "place value", "repair value")
        
        service_db = Service.objects.get(car=car)

        self.assertEqual("place value", service_db.place)
        self.assertEqual("repair value", service_db.repair)
        
    
    def test_get_service_by_id(self):

        add_few_cars_to_db()
        car = Car.objects.filter().first()

        service_id = ServiceFacade.add_new_service(car.id, "place value", "repair value", 12.50, "2020-06-23")
        
        service_db = ServiceFacade.get_service_by_id(service_id)

        self.assertEqual(service_id, service_db.id)
        self.assertEqual("place value", service_db.place)
        self.assertEqual("repair value", service_db.repair)
        self.assertEqual(12.50, service_db.cost)
        self.assertEqual( "2020-06-23", str(service_db.date))


    def test_get_service_by_id__id_not_exists(self):

        add_few_cars_to_db()
        cars = Car.objects.filter()

        service_id = ServiceFacade.add_new_service(cars[0].id, "place value", "repair value", 12.50, "2020-06-23")
        
        service = ServiceFacade.get_service_by_id(service_id+1)

        self.assertEqual(None, service)

    
    def test_get_car_services(self):
        
        car_service_ids = add_few_cars_and_services_to_db()

        # get id of first car from db
        car_id = list(car_service_ids.keys())[0]

        services = ServiceFacade.get_car_services(car_id)

        self.assertEqual(3, len(services))

        for i in range(1, len(services)+1):
            self.assertEqual("place service {} for car {}".format(i, car_id), services[i-1].place)
            self.assertEqual("repair service {} for car {}".format(i, car_id), services[i-1].repair)
            self.assertEqual("2019-05-12", str(services[i-1].date))
            self.assertEqual(110.50, services[i-1].cost)


    def test_get_car_services__car_not_exists(self):

        car_service_ids = add_few_cars_and_services_to_db()
        
        max_key = max(car_service_ids.keys())
        
        # the last one car is the car without services, but we want no existing car
        services = ServiceFacade.get_car_services(max_key+2)
        
        #pdb.set_trace()

        self.assertEqual(services, None)
        

    def test_get_car_services__services_not_exists(self):

        car_service_ids = add_few_cars_and_services_to_db()
        
        max_key = max(car_service_ids.keys())
        
        # the last one car is the car without services (this car is not present on car_service_ids)
        services = ServiceFacade.get_car_services(max_key+1)

        self.assertEqual(services, None)


    def test_edit_service(self):
        car_service_ids = add_few_cars_and_services_to_db()

        max_key = max(car_service_ids.keys())
        service_id = car_service_ids[max_key][0]

        service_old = Service.objects.get(id=service_id)

        car = Car.objects.get(id=max_key)

        #service_new = Service(place="new place", repair="new repair", cost=550.50, date="2022-12-15", car=car)

        ServiceFacade.edit_service(service_id, "new place", "new repair", 555.55, "2022-12-15", max_key)

        service_new = Service.objects.get(id=service_id)

        self.assertEqual(service_new.car.id, max_key)
        self.assertEqual(service_new.id, service_id)
        self.assertEqual(service_new.place, "new place")
        self.assertEqual(service_new.repair, "new repair")
        self.assertEqual(str(service_new.cost), str(555.55))
        self.assertEqual(str(service_new.date), "2022-12-15")


    def test_delete_service(self):
        car_service_ids = add_few_cars_and_services_to_db()

        service_id = car_service_ids[max(car_service_ids.keys())][0]

        delete_result = ServiceFacade.delete_service_by_id(service_id)

        self.assertEqual(tuple, type(delete_result))
        self.assertEqual(1, delete_result[0])

        with self.assertRaises(Service.DoesNotExist):
            del_service = Service.objects.get(id=service_id)

    
    def test_delete_service__service_not_exists(self):

        car_service_ids = add_few_cars_and_services_to_db()

        # get last service id + 1 from the last car
        service_id = max(car_service_ids[max(car_service_ids.keys())]) + 1

        delete_result = ServiceFacade.delete_service_by_id(service_id)

        self.assertEqual(None, delete_result)


    def test_check_service_user(self):
        car_service_ids = add_few_cars_and_services_to_db()

        car = Car.objects.get(id=list(car_service_ids.keys())[0])
        
        service_id = car_service_ids[car.id][0]

        result = ServiceFacade.check_service_user(service_id, car.user_id)

        self.assertTrue(result)


    def test_check_service_user__wrong(self):
        car_service_ids = add_few_cars_and_services_to_db()

        #pdb.set_trace()

        car = Car.objects.get(id=list(car_service_ids.keys())[0])
        
        service_id = car_service_ids[car.id][0]

        result = ServiceFacade.check_service_user(service_id, car.user_id+1)

        self.assertFalse(result)
       

class CarsAddCarViewTests(TestCase):
    
    def add_user_and_few_cars_to_db(self):
        self.client.post(reverse("register"), {"username": "gabriel", "email": "a@a.pl", "password1": "a", "password2": "a"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_1", "car_model": "Panda_1", "car_year": "2001"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_2", "car_model": "Panda_2", "car_year": "2002"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_3", "car_model": "Panda_3", "car_year": "2003"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_4", "car_model": "Panda_4", "car_year": "2004"})


    def test_add_car_GET(self):
        register_user_response = self.client.post(reverse("register"), {"username": "gabriel", "email": "a@a.pl", "password1": "a", "password2": "a"})

        add_car_response = self.client.get(reverse("cars:add_car"))

        self.assertIn("Add new car", str(add_car_response.content))
        self.assertEqual(add_car_response.status_code, 200)
        
    
    def test_add_car_POST(self):
        register_user_response = self.client.post(reverse("register"), {"username": "gabriel", "email": "a@a.pl", "password1": "a", "password2": "a"})
        add_car_response = self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_test_add_car_post", "car_model": "Panda", "car_year": "2004"})
        
        car_db = Car.objects.get(brand="Fiat_test_add_car_post")
                
        self.assertEqual(register_user_response.status_code, 302)
        self.assertEqual(add_car_response.status_code, 302)
        self.assertEqual(car_db.brand, "Fiat_test_add_car_post")
        self.assertEqual(car_db.model, "Panda")
        self.assertEqual(car_db.year, 2004)


    def test_get_user_cars(self):
        self.add_user_and_few_cars_to_db()

        response = self.client.get(reverse("cars:get_user_cars"))
                        
        self.assertIn('user_cars', response.context.keys())
        self.assertEqual("Fiat_1", response.context.get('user_cars')[0].brand)
        self.assertContains(response, "Fiat_3", status_code=200, html=True)


    def test_edit_car_GET(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.get(brand="Fiat_1")

        response = self.client.get(reverse("cars:edit_car", args=(car_db.id,)))

        self.assertIn('car_brand', response.context.keys())
        self.assertIn('car_model', response.context.keys())
        self.assertIn('car_id', response.context.keys())
        self.assertIn('car_year', response.context.keys())
        self.assertEqual('Fiat_1', response.context.get('car_brand'))
        self.assertEqual('Panda_1', response.context.get('car_model'))        

    
    def test_edit_car_POST(self):
        self.add_user_and_few_cars_to_db()

        car_db_before = Car.objects.get(brand="Fiat_1")

        response = self.client.post(reverse("cars:edit_car", \
        args=(car_db_before.id,)), \
        {"car_brand": "Fiat_111", "car_model": "Panda_111", "car_year": "2111"})

        car_db_after = Car.objects.get(id=car_db_before.id)

        self.assertEqual(car_db_after.brand, "Fiat_111")
        self.assertEqual(car_db_after.model, "Panda_111")
        self.assertEqual(car_db_after.year, 2111)
        self.assertEqual(response.status_code, 302)

    
    def test_delete_car_GET(self):
        self.add_user_and_few_cars_to_db()

        db_car = Car.objects.get(brand="Fiat_1")

        response = self.client.get(reverse("cars:delete_car", args=(db_car.id,)))

        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Car.DoesNotExist):
            del_car = Car.objects.get(id=db_car.id)

        
class ServiceViewTests(TestCase):

    def add_user_and_few_cars_to_db(self):
        self.client.post(reverse("register"), {"username": "gabriel", "email": "a@a.pl", "password1": "a", "password2": "a"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_1", "car_model": "Panda_1", "car_year": "2001"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_2", "car_model": "Panda_2", "car_year": "2002"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_3", "car_model": "Panda_3", "car_year": "2003"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_4", "car_model": "Panda_4", "car_year": "2004"})

    def add_user_cars_and_services_to_db(self):
        self.add_user_and_few_cars_to_db()

        cars = Car.objects.filter()

        for i, car in enumerate(cars):
            service_1 = Service(place="service place {}".format(i+1), repair="service repair {}".format(i+1), cost=120.20, date="2020-04-15", car=car)
            service_2 = Service(place="service place {}".format(i+2), repair="service repair {}".format(i+2), cost=120.20, date="2020-04-15", car=car)

            service_1.save()
            service_2.save()
    
    def test_add_service_GET(self):
        self.add_user_and_few_cars_to_db()
        car = Car.objects.first()
        
        add_service_response = self.client.get(reverse("cars:add_service", args=(str(car.id),)))

        self.assertEqual(200, add_service_response.status_code)
        self.assertIn("Add new service", str(add_service_response.content))

    def test_add_service_POST(self):
        self.add_user_and_few_cars_to_db()
        
        car = Car.objects.first()
        
        add_service_response = self.client.post(reverse("cars:add_service", args=(car.id,)), { 
            "service_place": "place of service",
            "service_repair": "repair of service",
            "service_cost": "220.50",
            "service_date": "1999-12-20"
            })

        service_db = Service.objects.filter(car_id=car.id).first()
        
        self.assertEqual(302, add_service_response.status_code)
        self.assertEqual("place of service", service_db.place)
        self.assertEqual("repair of service", service_db.repair)
        self.assertEqual(220.50, service_db.cost)
        self.assertEqual("1999-12-20", str(service_db.date))

    
    def test_get_car_services(self):
        
        self.add_user_cars_and_services_to_db()

        car_db = Car.objects.filter().first()

        response = self.client.get(reverse("cars:get_car_services", args=(car_db.id,)))

        services_db = Service.objects.filter(car=car_db)
        
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.context.get('car_services')))
        self.assertEqual(services_db[0].place, response.context.get('car_services')[0].place)
        self.assertEqual(services_db[0].repair, response.context.get('car_services')[0].repair)
        self.assertEqual(services_db[0].cost, response.context.get('car_services')[0].cost)
        self.assertEqual(services_db[0].date, response.context.get('car_services')[0].date)
        self.assertEqual(services_db[1].place, response.context.get('car_services')[1].place)
        self.assertEqual(services_db[1].repair, response.context.get('car_services')[1].repair)
        self.assertEqual(services_db[1].cost, response.context.get('car_services')[1].cost)
        self.assertEqual(services_db[1].date, response.context.get('car_services')[1].date)
        

    def test_edit_service_GET(self):
        self.add_user_cars_and_services_to_db()

        service_db = Service.objects.first()

        response = self.client.get(reverse("cars:edit_service", args=(service_db.id,)))

        self.assertEqual(200, response.status_code)
        self.assertInHTML("Edit service", str(response.content))
        self.assertIn('service', response.context.keys())
        self.assertEqual(service_db.place, response.context['service'].place)
        self.assertEqual(service_db.repair, response.context['service'].repair)
        self.assertEqual(service_db.cost, response.context['service'].cost)
        self.assertEqual(str(service_db.date), response.context['service'].date)

    
    def test_edit_service_POST(self):
        self.add_user_cars_and_services_to_db()

        service_db = Service.objects.first()

        response = self.client.post(reverse("cars:edit_service", args=(service_db.id,)), \
            {   "car_id": str(service_db.car.id), 
                "service_place": "service place test", 
                "service_repair": "service repair test",
                "service_cost": "2000.20", 
                "service_date": "2222-02-22"
                })
        
        service_db_after = Service.objects.get(id=service_db.id)

        self.assertEqual(302, response.status_code)
        self.assertEqual(service_db_after.place, "service place test")
        self.assertEqual(service_db_after.repair, "service repair test")
        self.assertEqual(str(service_db_after.cost), "2000.20")
        self.assertEqual(str(service_db_after.date), "2222-02-22")


    def test_move_service_GET(self):
        self.add_user_cars_and_services_to_db()

        service_db = Service.objects.first()

        response = self.client.get(reverse("cars:move_service", args=(service_db.id,)))

        #pdb.set_trace()
        self.assertEqual(200, response.status_code)        
        self.assertIn('user_cars', response.context.keys())
        

    def test_move_service_POST(self):
        self.add_user_cars_and_services_to_db()
        
        service_db = Service.objects.first()

        response = self.client.post(reverse("cars:move_service", args=(service_db.id,)), { "car_id": str(service_db.car.id+1) })

        self.assertEqual(302, response.status_code)

        service_db_after = Service.objects.get(id=service_db.id)

        self.assertEqual(service_db.car.id+1, service_db_after.car.id)


    def test_delete_service_GET(self):
        self.add_user_cars_and_services_to_db()

        service_db = Service.objects.first()

        response = self.client.get(reverse("cars:delete_service", args=(service_db.id,)))

        self.assertEqual(302, response.status_code)

        with self.assertRaises(Service.DoesNotExist):
            del_service = Service.objects.get(id=service_db.id)

        
class CarsViewApiTest(TestCase):

    def add_user_and_few_cars_to_db(self):
        self.client.post(reverse("register"), {"username": "gabriel", "email": "a@a.pl", "password1": "a", "password2": "a"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_1", "car_model": "Panda_1", "car_year": "2001"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_2", "car_model": "Panda_2", "car_year": "2002"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_3", "car_model": "Panda_3", "car_year": "2003"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_4", "car_model": "Panda_4", "car_year": "2004"})


    def test_add_car_api(self):
        self.add_user_and_few_cars_to_db()

        car = {
            "brand": "bbbb", 
            "model": "mmmm"
        }

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.post('/cars/add_car_api', car, format='json')
        client.logout()        

        self.assertEqual(201, response.status_code)
        self.assertTrue("car_id" in json.loads(response.content))

        car_id = json.loads(response.content)["car_id"]

        # raises exception if car does not exist in db
        Car.objects.get(id=car_id)
        
    
    def test_get_user_cars_api(self):
        self.add_user_and_few_cars_to_db()

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.get('/cars/get_user_cars_api', format='json')

        response_data = json.loads(response.content)

        #pdb.set_trace()
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, len(response_data))
        self.assertTrue('brand' in response_data[0])
        self.assertTrue('model' in response_data[1])
        self.assertTrue('year' in response_data[2])
        self.assertTrue('vin' in response_data[3])


    def test_edit_car_api(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.first()

        #car_to_change.brand = "new brand"
        #car_to_change.model = "new model"

        car_changed = {
            "brand": "new brand",
            "model": "new model",
            "car_id": car_db.id
        }

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.post('/cars/edit_car_api', car_changed, format='json')

        car_db_after = Car.objects.get(id=car_db.id)

        self.assertEqual(200, response.status_code)
        self.assertEqual("new brand", car_db_after.brand)
        self.assertEqual("new model", car_db_after.model)
        self.assertEqual(car_db.year, car_db_after.year)
        self.assertEqual(car_db.vin, car_db_after.vin)


    def test_edit_car_api_no_car(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.last()

        car_changed = {
            "brand": "new brand",
            "model": "new model",
            "car_id": car_db.id+100
        }

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.post('/cars/edit_car_api', car_changed, format='json')

        self.assertEqual(400, response.status_code)


    def test_delete_car_api(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.last()

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.delete('/cars/delete_car_api/{}'.format(car_db.id), format='json')

        self.assertEqual(200, response.status_code)

        with self.assertRaises(Car.DoesNotExist):
            del_car = Car.objects.get(id=car_db.id)

    
    def test_delete_car_api__car_not_exist(self):
        self.add_user_and_few_cars_to_db()

        car_db = Car.objects.last()

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.delete('/cars/delete_car_api/{}'.format(car_db.id+100), format='json')

        self.assertEqual(404, response.status_code)


class ServicesViewApiTest(TestCase):

    def add_user_and_few_cars_to_db(self):
        self.client.post(reverse("register"), {"username": "gabriel", "email": "a@a.pl", "password1": "a", "password2": "a"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_1", "car_model": "Panda_1", "car_year": "2001"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_2", "car_model": "Panda_2", "car_year": "2002"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_3", "car_model": "Panda_3", "car_year": "2003"})
        self.client.post(reverse("cars:add_car"), {"car_brand": "Fiat_4", "car_model": "Panda_4", "car_year": "2004"})


    def add_user_cars_and_services_to_db(self):
        self.add_user_and_few_cars_to_db()

        cars = Car.objects.filter()

        for i, car in enumerate(cars):
            service_1 = Service(place="service place {}".format(i+1), repair="service repair {}".format(i+1), cost=120.20, date="2020-04-15", car=car)
            service_2 = Service(place="service place {}".format(i+2), repair="service repair {}".format(i+2), cost=120.20, date="2020-04-15", car=car)

            service_1.save()
            service_2.save()


    def test_add_service_api(self):
        self.add_user_cars_and_services_to_db()

        car = Car.objects.first()

        service = {
            "place": "w",
            "repair": "r",
            "cost": 100.50,
            "date": "2021-02-10",
            "user_id": car.user_id,
            "car_id": car.id
        }

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.post('/cars/add_service_api', service, format='json')
        client.logout()

        created_service_id = response.data["service_id"]

        service_db = Service.objects.get(id=created_service_id)        
        
        self.assertEqual(201, response.status_code)
        self.assertEqual("w", service_db.place)
        self.assertEqual("r", service_db.repair)
        self.assertEqual(100.50, service_db.cost)
        self.assertEqual("2021-02-10", str(service_db.date))
        self.assertEqual(car.id, service_db.car.id)


    def test_add_service_api__wrong(self):
        self.add_user_cars_and_services_to_db()

        car = Service.objects.last()

        service = {
            "place": "w",
            "repair": "r",
            "cost": 100.50,
            "date": "2021-02-10",
            "user_id": 1,
            "car_id": car.id + 1
        }

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.post('/cars/add_service_api', service, format='json')
        client.logout()

        self.assertEqual(404, response.status_code)


    def test_get_car_services_api(self):
        self.add_user_cars_and_services_to_db()

        car = Car.objects.first()

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.get('/cars/get_car_services_api/{}'.format(car.id), format='json')
        response_data = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual('service place 1', response_data[0]['place'])
        self.assertEqual('service repair 1', response_data[0]['repair'])
        self.assertEqual("120.20", response_data[0]['cost'])
        self.assertEqual('2020-04-15', response_data[0]['date'])
        self.assertEqual('service place 2', response_data[1]['place'])
        self.assertEqual('service repair 2', response_data[1]['repair'])


    def test_edit_service_api(self):
        self.add_user_cars_and_services_to_db()

        service = Service.objects.first()

        service_changed = {
            "service_id": service.id,
            "place": "new place",
            "repair": "new repair",
            "cost": 500,
            "date": "2021-02-21"
        }

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.post('/cars/edit_service_api', service_changed, format='json')
        response_data = json.loads(response.content)

        # get service directly from db after change by method
        service_after = Service.objects.get(id=service.id)

        self.assertEqual(200, response.status_code)
        self.assertEqual(service_changed["service_id"], service_after.id)
        self.assertEqual(service_changed["place"], service_after.place)
        self.assertEqual(service_changed["repair"], service_after.repair)
        self.assertEqual(service_changed["cost"], service_after.cost)
        self.assertEqual(service_changed["date"], str(service_after.date))
    

    def test_edit_service_api__no_service(self):
        self.add_user_cars_and_services_to_db()

        service = Service.objects.last()

        service_changed = {
            "service_id": service.id + 1,
            "place": "new place",
            "repair": "new repair",
            "cost": 500,
            "date": "2021-02-21"
        }

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.post('/cars/edit_service_api', service_changed, format='json')
        response_data = json.loads(response.content)

        self.assertEqual(404, response.status_code)


    def test_delete_service_api(self):
        self.add_user_cars_and_services_to_db()

        service = Service.objects.last()

        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.delete('/cars/delete_service_api/{}'.format(service.id), format='json')

        self.assertEqual(200, response.status_code)

        with self.assertRaises(Service.DoesNotExist):
            del_service = Service.objects.get(id=service.id)


    def test_delete_service_api__service_not_exists(self):
        client = APIClient()
        client.login(username="gabriel", password="a")
        response = client.delete('/cars/delete_service_api/{}'.format(1), format='json')

        self.assertEqual(404, response.status_code)




