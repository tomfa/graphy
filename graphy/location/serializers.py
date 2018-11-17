from rest_framework import serializers

from graphy.location.models import County, Municipality, ZipCode, Address


class CountySerializer(serializers.ModelSerializer):
    country = serializers.CharField()

    class Meta:
        model = County
        fields = ('id', 'code', 'name', 'country')


class MunicipalitySerializer(serializers.ModelSerializer):
    county = CountySerializer()

    class Meta:
        model = Municipality
        fields = ('id', 'name', 'county')


class ZipCodeSerializer(serializers.ModelSerializer):
    county = CountySerializer()
    municipality = MunicipalitySerializer()

    class Meta:
        model = ZipCode
        fields = (
            'id',
            'code',
            'name',
            'municipality',
            'county',
        )


class AddressSerializer(serializers.ModelSerializer):
    zip_code = ZipCodeSerializer()
    country = serializers.CharField()

    class Meta:
        model = Address
        fields = (
            'id',
            'street_address',
            'zip_code',
            'country',
            'latitude',
            'longitude',
        )
