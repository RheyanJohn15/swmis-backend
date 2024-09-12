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
        elif method == 'deletetruck':
            self._deletetruck()
        elif method == 'deletedriver':
            self._deletedriver()
        elif method == 'truckdetail':
            self._truckdetail()
        elif method == 'driverdetail':
            self._driverdetail()
        elif method == 'updatetruck':
            self._updatetruck()
        elif method == 'updatedriver':
            self._updatedriver()

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

    def _deletetruck(self):
        truck_id = self.data.get('id')

        truck = Truck.objects.get(id=truck_id)

        truck.delete()

        newTruck = Truck.objects.all()
        
        serializeTruck = TruckSerializer(newTruck, many=True)

        for d in serializeTruck.data:
            d['deletelink'] = 'truckdriver/deletetruck/'
            d['editlink'] = 'truckdriver/updatetruck/'

        self.response = ['success', 'Successfully deleted truck', serializeTruck.data]

    def _deletedriver(self):

        driver_id = self.data.get('id')

        driver = Driver.objects.get(id = driver_id)

        driver.delete()

        newDriver = Driver.objects.all()

        serializeDriver = DriverSerializer(newDriver, many=True)
        
        for d in serializeDriver.data:
            d['deletelink'] = 'truckdriver/deletedriver/'
            d['editlink'] = 'truckdriver/updatedriver/'

        self.response = ['success', 'Successfully deleted driver', serializeDriver.data]

    def _truckdetail(self):
        
        truck_id = self.data.get('id')
        truck = Truck.objects.get(id=truck_id)
        serialize = TruckSerializer(truck)
        driver = Driver.objects.get(id=serialize.data['driver'])
        driverData = DriverSerializer(driver)

        self.response = ['success', 'Get Truck Details', dict(serialize.data, driverdata=driverData.data)]

    
    def _driverdetail(self):
        driver_id = self.data.get('id')

        driver = Driver.objects.get(id=driver_id)

        serialize = DriverSerializer(driver)

        self.response = ['success', 'Get Driver Detail', serialize.data]

    def _updatetruck(self):
        data = self.data

        truck = Truck.objects.get(id=data.get(id))

        truck.model = data.get('model')
        truck.plate_number = data.get('plate_number')
        truck.can_carry = data.get('can_carry')
        
        driver = Driver.objects.get(id=data.get('driver'))
        truck.driver = driver
        date = datetime.now()
        truck.updated_at = date

        truck.save()

        self.response = ['success', "Truck Details successfully updated", TruckSerializer(truck).data]

    def _updatedriver(self):
        data = self.data

        driver = Driver.objects.get(id=data.get("id"))

        driver.first_name = data.get('fname')
        driver.last_name = data.get('lname')
        driver.username = data.get('username')
        driver.license = data.get('license')
        driver.contact =data.get('contact')
        driver.address = data.get('address')
        driver.save()

        self.response = ['success', 'Driver Details successfully updated', DriverSerializer(driver).data]

    def result(self):
        return self.response