import graphene

from graphy.leads.gql_types import LeadType
from graphy.leads.models import Lead


class LeadQuery:
    lead = graphene.Field(LeadType, id=graphene.UUID())
    leads = graphene.List(LeadType, id=graphene.UUID(), email=graphene.String())

    def resolve_lead(self, info, **kwargs):
        return Lead.objects.filter(id=kwargs.get('id')).first()

    def resolve_leads(self, info, **kwargs):
        qs = Lead.objects.all()
        if 'email' in kwargs:
            email = kwargs.pop('email')
            qs = qs.filter(email__istartswith=email)
        return qs.filter(**kwargs)
