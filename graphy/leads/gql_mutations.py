import graphene

from graphene_django.rest_framework.mutation import SerializerMutation

from graphy.leads.gql_types import LeadType
from graphy.leads.serializers import LeadCreateSerializer


class LeadCreateMutation(SerializerMutation):
    lead = graphene.Field(LeadType)

    class Meta:
        serializer_class = LeadCreateSerializer

    @classmethod
    def perform_mutate(cls, serializer, info):
        lead = serializer.save()
        return cls(errors=None, lead=lead)
