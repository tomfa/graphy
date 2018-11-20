from graphy.leads.tests.conftest import *  # noqa


def test_customer_type(gql_client_staff, customer_with_user, lead):
    customer_with_user.leads.add(lead)

    query = """
        query($id: UUID!) {
          customer(id: $id) {
            id
            phoneNumber
            email
            user {
              id
            }
            leads {
              id
            }
            homeAddress {
              id
            }
          }
        }
    """
    params = {'id': str(customer_with_user.id)}

    result = gql_client_staff.execute(query, variables=params)

    customer_dict = result['data']['customer']
    assert customer_dict == {
        'id': str(customer_with_user.id),
        'phoneNumber': '+4741231234',
        'email': 'cake@example.com',
        'user': {'id': str(customer_with_user.user.id)},
        'leads': [{'id': str(lead.id)}],
        'homeAddress': {'id': str(customer_with_user.home_address.id)},
    }
