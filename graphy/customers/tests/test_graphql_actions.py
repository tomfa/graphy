def auth_error(path):
    return {
        'errors': [
            {
                'message': 'Authentication required.',
                'locations': [{'line': 3, 'column': 11}],
                'path': [path],
            }
        ],
        'data': {path: None},
    }


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

    assert result == auth_error('customer')


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

    assert result == auth_error('customers')


def test_customer_as_customer(gql_client_user, customer, customer_with_user):
    query = """
        query($id: UUID!) {
          customer(id: $id) {
            id
          }
        }
    """
    params = {'id': str(customer_with_user.id)}

    result = gql_client_user.execute(query, variables=params)

    assert result['data']['customer'] == {'id': str(customer_with_user.id)}


def test_all_customers_as_staff(gql_client_staff, customer):
    query = """
        query {
          customers {
            id
            email
          }
        }
    """

    result = gql_client_staff.execute(query)

    assert result['data']['customers'] == [
        {'id': str(customer.id), 'email': customer.email}
    ]


def test_customer_search_as_staff(
    gql_client_staff, customer, customer_with_user
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

    result = gql_client_staff.execute(query, variables=params)

    assert result['data']['customers'] == [
        {'id': str(customer.id), 'email': customer.email}
    ]
