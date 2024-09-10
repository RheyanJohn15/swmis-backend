from .API_Exception import ApiException
from django.http import JsonResponse
import json
from .API_Request import ApiRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class APIEntry:

    def __init__(self, request, type, method):
        self.request = request
        self.type = type
        self.method = method
        self.validated = False

    def get_response(self):
        self._check_validity()

        api_request = ApiRequest(self.type, self.method, self.request)

        return api_request.get_result()

    def _is_type_valid(self):
        return self.type in APIEntry.API_LIST

    def _is_method_valid(self):
        if self._is_type_valid():
            return self.method in APIEntry.API_LIST[self.type]
        return False

    def _check_validity(self):
        if not self._is_type_valid():
            raise ApiException(ApiException.INVALID_API)

        method_config = APIEntry.API_LIST[self.type].get(self.method)
        if not method_config:
            raise ApiException(ApiException.INVALID_API)

        # Check if the request method matches
        if self.request.method != method_config.get('method'):
            raise ApiException(ApiException.INVALID_API)

        # Check authentication requirements
        requires_authentication = method_config.get('requires_authentication', False)
        if requires_authentication:
        # Perform token-based authentication
            try:
                user = self._authenticate_with_token()
                if not user:
                    raise ApiException(ApiException.NOT_AUTHENTICATED)
                self.request.user = user  # Assign the authenticated user to the request
            except (InvalidToken, TokenError):
                raise ApiException(ApiException.NOT_AUTHENTICATED)

        # Initialize required_fields
        required_fields = method_config.get('required_fields', {})

        # Check required fields only if the method is not GET
        if self.request.method != 'GET':
            try:
                request_data = json.loads(self.request.body)
            except json.JSONDecodeError:
                raise ApiException(ApiException.INVALID_PARAMS)

        missing_fields = [field for field in required_fields if field not in request_data]

        if missing_fields:
            raise ApiException(ApiException.INVALID_PARAMS)

    def _authenticate_with_token(self):
        """
        Extracts and validates the JWT token from the Authorization header.
        Returns the user associated with the token if valid.
        Raises an exception if the token is invalid.
        """
        auth_header = self.request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise ApiException(ApiException.NOT_AUTHENTICATED)

        token = auth_header.split(' ')[1]

        jwt_auth = JWTAuthentication()
        validated_token = jwt_auth.get_validated_token(token)
        return jwt_auth.get_user(validated_token)

    API_LIST = {
        'user': {
            'login': {
                'required_fields': {
                    'username': 'string',
                    'password': 'string',
                },
                'requires_authentication': False,
                'method': 'POST'
            },
           
        },

        'truckdriver':{
             'addtruck': {
                'required_fields': {
                    'model': 'string',
                    'plate_number': 'string',
                    'can_carry': 'string',
                    'driver': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            },
             'adddriver': {
                'required_fields': {
                    'fname': 'string',
                    'lname': 'string',
                    'username': 'string',
                    'password': 'string',
                    'license': 'string',
                    'contact': 'string',
                    'address': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            },
            'listdriver': {
                'required_fields': {},
                'requires_authentication': True,
                'method': 'GET'
            },
             'listtruck': {
                'required_fields': {},
                'requires_authentication': True,
                'method': 'GET'
            },
            'updatetruck':{
                'required_fields': {
                    'id': 'string',
                    'model': 'string',
                    'plate_number': 'string',
                    'can_carry': 'string',
                    'driver': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            },
            'updatedriver':{
                'required_fields': {
                    'id': 'string',
                    'fname': 'string',
                    'lname': 'string',
                    'username': 'string',
                    'password': 'string',
                    'license': 'string',
                    'contact': 'string',
                    'address': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            },
            'deletedriver': {
                'required_fields': {
                    'id': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            },
            'deletetruck': {
                'required_fields': {
                    'id': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            },
            'truckdetail': {
                'required_fields': {
                    'id': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            },
            'driverdetail': {
                'required_fields': {
                    'id': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            }
        },

        'routes': {
            'add': {
                 'required_fields': {
                    'route_name': 'string',
                    'coordinates': 'string',
                    'driver': 'string',
                },
                'requires_authentication': True,
                'method': 'POST'
            },
            'list':{
                'required_fields': {},
                'requires_authentication': True,
                'method': 'GET'
            }
        },
        'complaints': {
            'sendmessage': {
                'required_fields': {
                    'complainant': 'string',
                    'contact': 'string',
                    'nature': 'string',
                    'remark': 'string'
                },
                'requires_authentication': False,
                'method': 'POST'
            },
             'list':{
                'required_fields': {},
                'requires_authentication': True,
                'method': 'GET'
            }
        }
        
    }