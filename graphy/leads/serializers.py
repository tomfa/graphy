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
