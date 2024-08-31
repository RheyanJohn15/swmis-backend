from django.http import JsonResponse
from .API_MODULES.API_Exception import ApiException

class CustomExceptionMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		try:
			response = self.get_response(request)
		except ApiException as e:
			return e.render()
		except Exception as e:
			# Handle other exceptions (optional)
			return JsonResponse({
				'status': 'error',
				'message': 'An unexpected error occurred: ' + str(e),
			}, status=500)
		return response