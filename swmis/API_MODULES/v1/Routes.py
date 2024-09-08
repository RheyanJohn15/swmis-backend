import json
from swmis.models import Routes, Driver
from swmis.serializers import RouteSerializer
class RoutesClass:
    def __init__(self, method, request):
        
        if request.method != 'GET':
            self.data = json.loads(request.body)
        
        if method == 'add':
            self._add()
        elif method == 'list':
            self._list()
    
    def _add(self):
        data = self.data
        
        driver_instance = Driver.objects.get(id=data.get('driver'))

        route = Routes(
            route_name = data.get('route_name'),
            coordinates = data.get('coordinates'),
            driver = driver_instance
        )

        route.save()

        serialize = RouteSerializer(route)

        self.response = ['success', 'Successfull added route', serialize.data]

    def _list(self):
        routes = Routes.objects.all()

        serialize = RouteSerializer(routes, many=True)

        for d in serialize.data:
            d['deletelink'] = 'routes/delete/'
            d['editlink'] = 'routes/update/'

        self.response = ['success','Get all routes', serialize.data]

    def result(self):
        return self.response
