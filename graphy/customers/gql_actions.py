from django.db.models import Q
import graphene

from graphy.customers.gql_types import CustomerType
from graphy.customers.models import Customer
from graphy.utils.graphql import auth_required


class CustomerQuery:
    customer = graphene.Field(CustomerType, id=graphene.UUID())
    customers = graphene.List(
        CustomerType, id=graphene.UUID(), email=graphene.String()
    )

    @auth_required
    def resolve_customer(self, info, **kwargs):
        return Customer.objects.filter(id=kwargs.get('id')).first()

    @auth_required
    def resolve_customers(self, info, **kwargs):
        qs = Customer.objects.all()
        if 'email' in kwargs:
            email = kwargs.pop('email')
            qs = qs.filter(
                Q(email__istartswith=email) | Q(user__email__startswith=email)
            )
        return qs.filter(**kwargs)
