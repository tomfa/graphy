import pytest


@pytest.mark.xfail(
    strict=True, reason='Anonymous gql client should not see customers'
)
def test_customer_as_anonymous(gql_client, customer):
    query = """
        query($id: UUID!) {
          customer(id: $id) {
            id
          }
        }
    """
    params = {'id': str(customer.id)}

    result = gql_client.execute(query, variables=params)

    assert result['data']['customer'] == {'id': str(customer.id)}


@pytest.mark.xfail(
    strict=True, reason='Anonymous gql client should not see customers'
)
def test_all_customers_as_anonymous(gql_client, customer):
    query = """
        query {
          customers {
            id
            email
          }
        }
    """

    result = gql_client.execute(query)

    assert result['data']['customers'] == [
        {'id': str(customer.id), 'email': customer.email}
    ]


@pytest.mark.xfail(
    strict=True, reason='Anonymous gql client should not see customers'
)
def test_customer_search_as_anonymous(
    gql_client, customer, customer_with_user
):
    query = """
        query($email: String) {
          customers(email: $email) {
            id
            email
          }
        }
    """
    params = {'email': customer.email}

    result = gql_client.execute(query, variables=params)

    assert result['data']['customers'] == [
        {'id': str(customer.id), 'email': customer.email}
    ]
