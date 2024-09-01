import json
from swmis.models import Driver, Truck
from datetime import datetime
from swmis.serializers import TruckSerializer, DriverSerializer
class TruckDriver:

    def __init__(self, method, request):
        self.data = json.loads(request.body)

        if method == 'addtruck':
            self._addtruck()
        elif method == 'adddriver':
            self._adddriver()

    
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

        self.response = ['success', 'Driver Successfully added to the system', DriverSerializer(driver).data ]
    
    def _addtruck(self):
        data = self.data
        truck = Truck(
            model = data.get('model'),
            plate_number = data.get('plate_number'),
            can_carry = data.get('can_carry'),
            driver = data.get('driver'),
            created_at = datetime.now(),
            updated_at = datetime.now()
        )

        truck.save()

        self.response = ['success', 'Truck Successfully added to the system', TruckSerializer(truck).data]

    def result(self):
        return self.response