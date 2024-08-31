import json
from swmis.API_MODULES.API_Exception import ApiException
from swmis.models import UserAccount
from swmis.serializers import UserAccountSerializer
from swmis.API_MODULES.Helper import Helper
from django.contrib.auth.hashers import check_password
class User:

	def __init__(self, method, request):
		self.data = json.loads(request.body)

		if method == 'login':
			self._login()

	def _login(self):
		
		try:
			user = UserAccount.objects.get(username = self.data.get('username'))

			if check_password(self.data.get('password'), user.password):
				tokens = Helper.generate_tokens(user)
				self.response = ['success', 'Login Successfully', tokens]
			else:
				raise ApiException(ApiException.PASSWORD_INVALID)
		except UserAccount.DoesNotExist:
			raise ApiException(ApiException.USERNAME_INVALID)
			

	def result(self):
		return self.response