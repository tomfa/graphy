import json

from graphy.customers.tests.conftest import *  # noqa
from graphy.leads.tests.conftest import *  # noqa


def test_can_query_with_depth_7(drf_client_staff, address, customer, lead):
    """
    This test looks a bit funky. Our gql_client fixture does not include the
    depth analyzer. The endpoint on our server does however
    """
    lead.address = address
    lead.save()
    customer.leads.add(lead)
    expected_county_id = customer.home_address.zip_code.municipality.county_id
    query = """
        query {
          customers {
            homeAddress {
              zipCode {
                municipality {
                  county {
                    id
                  }
                }
              }
            }
          }
        }
    """

    result = drf_client_staff.post(
        '/graphql/?',
        data={'operationName': 'null', 'query': query, 'variables': 'null'},
    )
    assert json.loads(result._container[0])['data']['customers'] == [
        {
            'homeAddress': {
                'zipCode': {
                    'municipality': {
                        'county': {
                            'id': str(expected_county_id)
                        }
                    }
                }
            }
        }
    ]


def test_can_not_query_with_depth_8(drf_client_staff, address, customer, lead):
    """
    This test looks a bit funky. Our gql_client fixture does not include the
    depth analyzer. The endpoint on our server does however
    """
    lead.address = address
    lead.save()
    customer.leads.add(lead)

    query = """
        query {
          customers {
            leads {
              address {
                zipCode {
                  municipality {
                    county {
                      id
                    }
                  }
                }
              }
            }
          }
        }
    """

    result = drf_client_staff.post(
        '/graphql/?',
        data={'operationName': 'null', 'query': query, 'variables': 'null'},
    )

    assert json.loads(result._container[0]) == {
        'errors': [{'message': 'Query is too complex'}]
    }
