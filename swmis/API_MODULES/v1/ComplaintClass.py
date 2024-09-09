import json
from swmis.models import Complaints
from swmis.serializers import ComplaintSerializer

class ComplaintClass:
    
    def __init__(self, method, request):
        
        if request.method != 'GET':
            self.data = json.loads(request.body)
        
        if method == 'sendmessage':
            self._sendmessage()
        if method == 'list':
            self._list()

    def _sendmessage(self):
        data = self.data

        comp = Complaints(
            complainant = data.get('complainant'),
            contact = data.get('contact'),
            nature = data.get('nature'),
            remarks = data.get('remark')
        )

        comp.save()

        self.response = ['success', 'Complaint sent Successfully', 'null']

    def _list(self):
        comp = Complaints.objects.all()

        serialize = ComplaintSerializer(comp, many=True)
        
        for d in serialize.data:
            d['deletelink'] = 'complaints/delete'
            d['editlink'] = 'complaints/update'

        self.response = ['success', 'Get all complaints', serialize.data]

    def result(self):
        return self.response