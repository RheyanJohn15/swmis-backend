from rest_framework import serializers
from .models import UserAccount



class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'name',
            'password',
            'user_type',
            'created_at',
            'user_status',
        ]
