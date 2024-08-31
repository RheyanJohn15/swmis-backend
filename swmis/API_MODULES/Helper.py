from rest_framework_simplejwt.tokens import RefreshToken
from swmis.models import RefreshToken as CustomRefreshToken  # Import the custom RefreshToken model
import datetime
from django.utils import timezone
from swmis.serializers import UserAccountSerializer

class Helper:
    def __init__(self):
        pass

    @staticmethod
    def generate_tokens(user):
        # Generate refresh and access tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        serialize = UserAccountSerializer(user)
        # Save the refresh token to the database
        CustomRefreshToken.objects.create(
            token=str(refresh),
            user=user,
            expires_at=timezone.now() + datetime.timedelta(days=7)  # Example expiration period
        )

        return {
            'refresh': str(refresh),
            'access': str(access),
            'account': serialize.data
        }