from graphene_django import DjangoObjectType

from graphy.leads.models import Lead


class LeadType(DjangoObjectType):
    class Meta:
        model = Lead
        only_fields = (
            'id',
            'email',
            'address',
            'uncleaned_address',
            'utm_campaign',
            'utm_medium',
            'utm_source',
        )
