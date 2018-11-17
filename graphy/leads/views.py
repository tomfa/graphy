from rest_framework import viewsets, permissions, mixins

from graphy.leads.models import Lead
from graphy.leads.serializers import LeadRegistrationSerializer, LeadSerializer


class LeadAPIViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LeadRegistrationSerializer
        return LeadSerializer

    def get_queryset(self):
        return Lead.objects.all()
