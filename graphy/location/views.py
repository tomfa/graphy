from rest_framework import viewsets, permissions, mixins

from graphy.location.serializers import CountySerializer
from graphy.location.models import County


class CountyAPIViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = CountySerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return County.objects.prefetch_related('municipality_set')
