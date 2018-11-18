import graphene

from graphy.location import gql_actions as location_actions


class Query(
    graphene.ObjectType,
    location_actions.AddressQuery,
    location_actions.CountyQuery,
):
    pass


schema = graphene.Schema(query=Query)
