from rest_framework import viewsets, mixins, permissions

from graphy.customers.models import Customer
from graphy.customers.serializers import CustomerSerializer


class CustomerViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return CustomerSerializer

    def get_queryset(self):
        return Customer.all_for_user(self.request.user)

