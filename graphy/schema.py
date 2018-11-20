import graphene

from graphy.customers import gql_actions as customer_actions
from graphy.leads import gql_actions as lead_actions
from graphy.location import gql_actions as location_actions


class Query(
    graphene.ObjectType,
    customer_actions.CustomerQuery,
    location_actions.AddressQuery,
    location_actions.CountyQuery,
    lead_actions.LeadQuery,
):
    pass


class Mutation(graphene.ObjectType, lead_actions.LeadMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
