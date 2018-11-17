from rest_framework import viewsets, permissions, mixins

from graphy.location.serializers import (
    AddressSerializer,
    CountySerializer,
    MunicipalitySerializer,
    ZipCodeSerializer,
)
from graphy.location.models import Address, County, ZipCode


class CountyAPIViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    serializer_class = CountySerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return County.objects.prefetch_related('municipality_set')


class ZipCodeAPIViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    serializer_class = ZipCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return ZipCode.objects.select_related('county', 'municipality')


class AddressAPIViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    serializer_class = AddressSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Address.objects.select_related('zip_code')
