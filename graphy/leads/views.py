from rest_framework import viewsets, permissions, mixins

from graphy.leads.models import Lead
from graphy.leads.serializers import LeadSerializer


class LeadAPIViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    serializer_class = LeadSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Lead.objects.all()
