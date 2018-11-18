def test_address(gql_client, address):
    query = """
        query($id: UUID!) {
          address(id: $id) {
            id 
          }
        }
    """
    params = {'id': str(address.id)}

    result = gql_client.execute(query, variables=params)

    assert result['data']['address'] == {'id': str(address.id)}


def test_addresses(gql_client, address):
    query = """
        query {
          addresses {
            id 
          }
        }
    """
    params = {'id': str(address.id)}

    result = gql_client.execute(query, variables=params)

    assert result['data']['addresses'] == [{'id': str(address.id)}]


def test_county(gql_client, county):
    query = """
        query($id: UUID!) {
          county(id: $id) {
            id 
          }
        }
    """

    params = {'id': str(county.id)}
    result = gql_client.execute(query, variables=params)
    assert result['data']['county'] == {'id': str(county.id)}


def test_counties(gql_client, county):
    query = """
        query {
          counties {
            id 
          }
        }
    """

    params = {'id': str(county.id)}
    result = gql_client.execute(query, variables=params)
    assert result['data']['counties'] == [{'id': str(county.id)}]
