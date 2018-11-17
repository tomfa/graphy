from rest_framework import serializers

from graphy.leads.models import Lead
from graphy.location.serializers import AddressSerializer


class LeadSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Lead
        fields = (
            'id',
            'email',
            'address',
            'uncleaned_address',
            'utm_campaign',
            'utm_medium',
            'utm_source',
        )


class LeadRegistrationSerializer(serializers.Serializer):
    address = serializers.CharField(min_length=8, max_length=64)
    email = serializers.EmailField(max_length=254)
    utm_campaign = serializers.CharField(required=False, max_length=64)
    utm_medium = serializers.CharField(required=False, max_length=64)
    utm_source = serializers.CharField(required=False, max_length=64)

    def validate_address(self, address):
        if ',' not in address:
            raise serializers.ValidationError(
                'Any address with respect for itself has atleast one comma.'
            )
        return address.lower()

    def create(self, validated_data):
        uncleaned_address = validated_data.pop('address')
        return Lead.objects.create(
            uncleaned_address=uncleaned_address,
            **validated_data
        )
