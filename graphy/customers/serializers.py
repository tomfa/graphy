from django.contrib.auth import get_user_model
from rest_framework import serializers

from graphy.customers.models import Customer


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'is_staff',
        )


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = (
            'id',
            'email',
            'phone_number',
            'user',
            'leads',
        )
