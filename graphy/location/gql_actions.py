import graphene

from graphy.location.gql_types import AddressType, CountyType
from graphy.location.models import Address, County


class CountyQuery:
    county = graphene.Field(CountyType, id=graphene.UUID())
    counties = graphene.List(
        CountyType, id=graphene.UUID(), name=graphene.String()
    )

    def resolve_county(self, info, **kwargs):
        return County.objects.filter(id=kwargs.get('id')).first()

    def resolve_counties(self, info, **kwargs):
        qs = County.objects.all()
        return qs.filter(**kwargs)


class AddressQuery:
    address = graphene.Field(AddressType, id=graphene.UUID())
    addresses = graphene.List(
        AddressType, id=graphene.UUID(), street_address=graphene.String()
    )

    def resolve_address(self, info, **kwargs):
        return Address.objects.filter(id=kwargs.get('id')).first()

    def resolve_addresses(self, info, **kwargs):
        qs = Address.objects.all()
        if 'street_address' in kwargs:
            street_address = kwargs.pop('street_address')
            qs = qs.filter(street_address__istartswith=street_address)
        return qs
