from django.http import JsonResponse
from django.middleware.csrf import get_token
from .API_MODULES.API_Verification import APIEntry
from .API_MODULES.API_Exception import ApiException

def index(request, type, method):
    if type == 'csrf' and method == 'get':
        csrf_token = get_token(request)
        response_data = {
            'status': 'success',
            'csrfToken': csrf_token
        }
    else:
        api_entry = APIEntry(request, type, method)
        try:
            response_data = api_entry.get_response()
        except ApiException as e:
            return e.render() 

    return JsonResponse(response_data, status=200)