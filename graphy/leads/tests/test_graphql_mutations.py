def test_lead_create(gql_client, lead):
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
    email = 'Tomas@otovo.com'
    address = 'Torggata 5, 0181 Oslo'
    params = {'email': email, 'address': address}

    result = gql_client.execute(query, variables=params)

    lead = result['data']['createLead']['lead']
    assert lead['id']

    # Input made lower by DRF serializer .validate_() methods
    assert lead['email'] == email.lower()
    assert lead['uncleanedAddress'] == address.lower()


def test_leads_email_search(gql_client, lead):
    query = """
        query($email: String) {
          leads(email: $email) {
            id
            email 
          }
        }
    """
    params = {'email': lead.email}

    result = gql_client.execute(query, variables=params)

    assert result['data']['leads'] == [
        {'id': str(lead.id), 'email': lead.email}
    ]


def test_leads_email_search_no_results(gql_client, lead):
    query = """
        query($email: String) {
          leads(email: $email) {
            id
            email 
          }
        }
    """
    params = {'email': f'{lead.email}cheese'}

    result = gql_client.execute(query, variables=params)

    assert result['data']['leads'] == []
