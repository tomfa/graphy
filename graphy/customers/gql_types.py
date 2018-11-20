from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

from graphy.customers.models import Customer


class UserType(DjangoObjectType):
    full_name = graphene.String(source='get_full_name')

    class Meta:
        model = get_user_model()
        only_fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'is_staff',
        )


class CustomerType(DjangoObjectType):
    phone_number = graphene.String()

    class Meta:
        model = Customer
        only_fields = (
            'id',
            'email',
            'user',
            'leads',
            'home_address',
        )

    def resolve_phone_number(self, info, **kwargs):
        """
        GOTCHA: This is the only resolve method we have on a type
        in this repository.
        - self is the instance of the Customer object.
        - the info variable contains context, which is pretty equal to request
          variable in regular django views. The user object is e.g. located at
          info.context.user
        - for certain fields and values, we have to create resolvers, even
          when it seems unnecessary: we just cast to string here, which
          graphene should already know due to its field declaration.
          This also applies to @properties
        """
        return str(self.phone_number)
