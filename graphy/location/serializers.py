from rest_framework import serializers

from graphy.location.models import County


class CountySerializer(serializers.ModelSerializer):
    country = serializers.CharField()

    class Meta:
        model = County
        fields = (
            'id',
            'created_at',
            'updated_at',
            'code',
            'name',
            'country',
        )
