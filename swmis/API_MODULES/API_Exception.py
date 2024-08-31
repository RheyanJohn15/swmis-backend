from django.http import JsonResponse

class ApiException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def render(self):
        return JsonResponse({
            'status': 'fail',
            'message': self.message,
        }, status=400)

    # Define custom exception messages
    NOT_AUTHENTICATED = 'Cannot Access API, not authenticated'
    NO_DATA_FOUND = 'No data found in this API request'
    INVALID_PARAMS = 'The parameter body is incomplete or invalid'
    INVALID_API = 'The API URL is invalid'
    USERNAME_INVALID = 'The username is not registered'
    PASSWORD_INVALID = 'Password does not match'