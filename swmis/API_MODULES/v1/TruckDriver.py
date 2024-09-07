import json
from swmis.models import Driver, Truck
from datetime import datetime
from swmis.serializers import TruckSerializer, DriverSerializer
class TruckDriver:

    def __init__(self, method, request):
        
        if request.method != 'GET':
            self.data = json.loads(request.body)

        if method == 'addtruck':
            self._addtruck()
        elif method == 'adddriver':
            self._adddriver()
        elif method == 'listdriver':
            self._listdriver()
        elif method == 'listtruck':
            self._listtruck()
        

    
    def _adddriver(self):
        data = self.data
        driver = Driver(
            first_name = data.get('fname'),
            last_name = data.get('lname'),
            username = data.get('username'),
            password = data.get('password'),
            license = data.get('license'),
            contact = data.get('contact'),
            address = data.get('address'),
            created_at = datetime.now(),
            updated_at = datetime.now()
        )

        driver.save()
        serialize =  DriverSerializer(driver)

        self.response = ['success', 'Driver Successfully added to the system', serialize.data ]
    
    def _addtruck(self):
        data = self.data
        driver_instance = Driver.objects.get(id=data.get('driver'))
        truck = Truck(
            model = data.get('model'),
            plate_number = data.get('plate_number'),
            can_carry = data.get('can_carry'),
            driver = driver_instance,
            created_at = datetime.now(),
            updated_at = datetime.now()
        )

        truck.save()

        self.response = ['success', 'Truck Successfully added to the system', TruckSerializer(truck).data]

    def _listdriver(self):
        driver = Driver.objects.all()

        serialize = DriverSerializer(driver, many=True)
        for d in serialize.data:
            d['deletelink'] = 'truckdriver/deletedriver/'
            d['editlink'] = 'truckdriver/updatedriver/'

        self.response = ['success', 'Get all Driver data', serialize.data]

    def _listtruck(self):
        truck = Truck.objects.all()

        serialize = TruckSerializer(truck, many=True)
        for d in serialize.data:
            d['deletelink'] = 'truckdriver/deletetruck/'
            d['editlink'] = 'truckdriver/updatetruck/'

        self.response = ['success', 'Get all truck data', serialize.data]

    def result(self):
        return self.response