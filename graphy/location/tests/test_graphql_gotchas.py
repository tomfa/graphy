def test_enum_becomes_uppercase(gql_client, address, county):
    """
    Both AddressType and CountyType has a Country enum field.
    AddressType has explicitly set it as graphene.String() while
    CountyType is left to determine it by itself.

    Graphene follows the seems to convention in GraphQL examples, uppercase it
    https://github.com/graphql-python/graphene-django/issues/280

    Gotcha:
    In transferring front end code from DRF to graphene, choices fields
    needs to be defined as CharField, or enums needs to be refactored to
    uppercase, atleast in frontend code.
    """

    address_query = """
        query($id: String!) {
          address(id: $id) {
            country
          }
        }
    """
    county_query = """
        query($id: String!) {
          county(id: $id) {
            country
          }
        }
    """

    gql_address_country = gql_client.execute(
        address_query, variables={'id': str(address.id)}
    )['data']['address']['country']

    gql_county_country = gql_client.execute(
        county_query, variables={'id': str(county.id)}
    )['data']['county']['country']

    assert county.country == address.country
    assert gql_address_country == 'no'
    assert gql_county_country == 'NO'
