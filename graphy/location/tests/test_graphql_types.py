def test_address_type(gql_client, address):
    query = """
        query($id: String!) {
          address(id: $id) {
            id 
            country
            streetAddress
            latitude
            longitude
            zipCode {
              id 
            }
          }
        }
    """
    params = {'id': str(address.id)}

    result = gql_client.execute(query, variables=params)

    address_dict = result['data']['address']
    assert address_dict == {
        'id': str(address.id),
        'streetAddress': address.street_address,
        'latitude': address.latitude,
        'longitude': address.longitude,
        'country': str(address.country),
        'zipCode': {'id': str(address.zip_code.id)},
    }


def test_county_type(gql_client, county):
    query = """
        query($id: String!) {
          county(id: $id) {
            id 
            name 
            code 
            country
          }
        }
    """

    params = {'id': str(county.id)}
    result = gql_client.execute(query, variables=params)
    county_dict = result['data']['county']
    assert county_dict == {
        'id': str(county.id),
        'name': county.name,
        'code': county.code,
        'country': 'NO',
    }


def test_municipality_type(gql_client, address):
    query = """
        query($id: String!) {
          address(id: $id) {
            zipCode {
              municipality {
                id
                name
                county {
                  id
                }
              }
            }
          }
        }
    """
    params = {'id': str(address.id)}

    result = gql_client.execute(query, variables=params)

    municipality = address.zip_code.municipality
    municipality_dict = result['data']['address']['zipCode']['municipality']
    assert municipality_dict == {
        'id': str(municipality.id),
        'name': municipality.name,
        'county': {'id': str(municipality.county.id)},
    }


def test_zipcode_type(gql_client, address):
    query = """
        query($id: String!) {
          address(id: $id) {
            zipCode {
              id 
              code 
              name 
              municipality {
                id
              }
              county {
                id
              }
            }
          }
        }
    """
    params = {'id': str(address.id)}

    result = gql_client.execute(query, variables=params)

    zip_code_dict = result['data']['address']['zipCode']
    assert zip_code_dict == {
        'id': str(address.zip_code.id),
        'name': address.zip_code.name,
        'code': address.zip_code.code,
        'municipality': {'id': str(address.zip_code.municipality.id)},
        'county': {'id': str(address.zip_code.county.id)},
    }
