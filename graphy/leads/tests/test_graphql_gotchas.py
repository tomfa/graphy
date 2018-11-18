import json


def test_lead_query_returns_error_on_root_level(gql_client, lead):
    query = """
        query($id: UUID!) {
          lead(id: $id) {
            id 
          }
        }
    """
    params = {'id': 'not-an-uuid'}

    result = gql_client.execute(query, variables=params)

    # Note: no data key in result, only error
    assert result == {
        'errors': [{'message': 'badly formed hexadecimal UUID string'}]
    }


def test_lead_create_invalid_address_missing_error(gql_client, lead):
    query = """
        mutation($address: String!, $email: String!) {
          createLead(input: {
            email: $email,
            address: $address,
          }) {
            lead {
              id
              email
              uncleanedAddress
            }
          }
        }
    """
    email = 'invalid email'
    address = 'This address has no comma'
    params = {'email': email, 'address': address}

    result = gql_client.execute(query, variables=params)

    assert result == {'data': {'createLead': {'lead': None}}}


def test_lead_create_invalid_address_with_error(gql_client, lead):
    # Note: we have to ask for errors specifically
    query = """
        mutation($address: String!, $email: String!) {
          createLead(input: {
            email: $email,
            address: $address,
          }) {
            errors {
              messages
            }
            lead {
              id
              email
              uncleanedAddress
            }
          }
        }
    """
    email = 'invalid email'
    address = 'This address has no comma'
    params = {'email': email, 'address': address}

    # Note: different error object structure than with Query
    expected_errors = [
        {
            'messages': [
                'Any address with respect for itself has atleast one comma.'
            ]
        },
        {'messages': ['Enter a valid email address.']},
    ]

    result = gql_client.execute(query, variables=params)

    # Note: Errors specified inside data -> createLead, not in errors object
    # on root level, as with Query
    assert json.loads(json.dumps(result)) == {
        'data': {'createLead': {'errors': expected_errors, 'lead': None}}
    }
