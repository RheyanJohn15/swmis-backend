from .v1.User import User
from datetime import datetime
class ApiRequest:

	def __init__(self, type, method, request):
		self.type = type
		self.method = method
		self.request = request

	def _user(self):
		action = User(self.method, self.request)
		return action.result()

	switch_dict = {
		'user': '_user',
	}
	
	def switch(self):
		method_name = self.switch_dict.get(self.type, 'default_case')
		method = getattr(self, method_name)
		return method()

	def default_case(self):
		return ['error', 'Invalid type', None]
	
	def get_result(self):
		data = self.switch()

		now = datetime.now().isoformat()  # Add current time
		response_data = {
			'status': data[0],
			'message': data[1],
			'current_time': now,
			'data': data[2]
		}
		return response_data