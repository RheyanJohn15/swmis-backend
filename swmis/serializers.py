from rest_framework import serializers
from .models import UserAccount, Truck, Driver



class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'name',
            'user_type',
            'created_at',
            'user_status',
        ]

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'license',
            'contact',
            'address',
            'created_at',
            'updated_at',
        ]

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = [
         'id',
         'model',
         'plate_number',
         'can_carry',
         'driver',
         'status',
         'created_at',
         'updated_at'   
        ]