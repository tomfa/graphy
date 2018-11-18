def test_lead(gql_client, lead):
    query = """
        query($id: UUID!) {
          lead(id: $id) {
            id 
          }
        }
    """
    params = {'id': str(lead.id)}

    result = gql_client.execute(query, variables=params)

    assert result['data']['lead'] == {'id': str(lead.id)}


def test_leads(gql_client, lead):
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
