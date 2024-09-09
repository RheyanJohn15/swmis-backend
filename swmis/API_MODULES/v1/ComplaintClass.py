import json
from swmis.models import Complaints
from swmis.serializers import ComplaintSerializer

class ComplaintClass:
    
    def __init__(self, method, request):
        
        if request.method != 'GET':
            self.data = json.loads(request.body)
        
        if method == 'sendmessage':
            self._sendmessage()

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

    def result(self):
        return self.response