from random import random
import uuid

from graphy.location.tests.conftest import *  # noqa


SHALLOW_GQL_ADDRESS_QUERY = """
    query {
      addresses {
        id
        streetAddress
        country
        latitude
        longitude
      }
    }
"""

DEEP_GQL_ADDRESS_QUERY = """
    query {
      addresses {
        id
        streetAddress
        country
        latitude
        longitude
        zipCode {
          id
          code
          name
          municipality {
            id
            name
            county {
              id
              name
              code
              country
            }
          }
          county {
            id
            name
            code
            country
          }
        }
      }
    }
"""


@pytest.fixture
def address_generator_with_same_zip(country, zip_code):
    def create_address():
        return Address.objects.create(
            street_address=f'{str(uuid.uuid4())[:8]} Avenue',
            zip_code=zip_code,
            country=country,
            latitude=Decimal(60 * random()),
            longitude=Decimal(60 * random()),
        )

    return create_address


@pytest.fixture
def reset_addresses(address_generator_with_same_zip):
    # Used for repopulating to prevent any form of DB caching
    def fun(*, num_addresses):
        Address.objects.all().delete()
        for i in range(num_addresses):
            address_generator_with_same_zip()
        assert Address.objects.count() == num_addresses

    return fun


@pytest.fixture
def performance_tester(drf_client, gql_client, reset_addresses):
    """
    Tests performance for a gql_query vs DRF address
    list with and without select_related.

    The results should be taken with a some large grains of salt,
    as they use DRF and graphene test clients rather than being run
    at the server endpoints. See README.md for results for a fairer
    comparison.
    """

    def get_time_spent(*, num_addresses):
        reset_addresses(num_addresses=num_addresses)
        drf_time = timing(lambda: drf_client.get('/location/addresses/'))
        reset_addresses(num_addresses=num_addresses)
        drf_related_time = timing(
            lambda: drf_client.get('/location/addresses/?select_related')
        )
        reset_addresses(num_addresses=num_addresses)
        gql_deep_time = timing(
            lambda: gql_client.execute(DEEP_GQL_ADDRESS_QUERY)
        )

        reset_addresses(num_addresses=num_addresses)
        gql_shallow_time = timing(
            lambda: gql_client.execute(SHALLOW_GQL_ADDRESS_QUERY)
        )

        return {
            'gql_shallow_time': gql_shallow_time,
            'gql_deep_time': gql_deep_time,
            'drf_time': drf_time,
            'drf_related_time': drf_related_time,
        }

    return get_time_spent


def test_deep_gql_query_is_same_sql_as_drf(address, drf_client, gql_client):
    # Note: DRF without select related
    drf_sql = queries(lambda: drf_client.get('/location/addresses/'))
    gql_sql = queries(lambda: gql_client.execute(DEEP_GQL_ADDRESS_QUERY))

    assert drf_sql == gql_sql


@pytest.mark.skip(reason='Performance tests can not be trusted')
def test_performance_100_addresses(performance_tester):
    time = performance_tester(num_addresses=100)

    print(time)  # For easier checking when test fails
    assert sorted(time.values()) == [
        time['gql_shallow_time'],
        time['drf_related_time'],
        time['drf_time'],
        time['gql_deep_time'],
    ]


@pytest.mark.skip(reason='Performance tests can not be trusted')
def test_performance_1_address(performance_tester):
    time = performance_tester(num_addresses=100)

    print(time)  # For easier checking when test fails
    assert sorted(time.values()) == [
        time['gql_shallow_time'],
        time['drf_related_time'],
        time['drf_time'],
        time['gql_deep_time'],
    ]


@pytest.mark.skip(reason='Performance tests can not be trusted')
def test_print_repeated_library_performance(performance_tester):
    num_runs = 10

    gql_shallow_total = 0
    gql_deep_total = 0
    drf_total = 0
    drf_related_total = 0

    for i in range(num_runs):
        time = performance_tester(num_addresses=1)
        drf_total += time['drf_time']
        gql_shallow_total += time['gql_shallow_time']
        gql_deep_total += time['gql_deep_time']
        drf_related_total += time['drf_related_time']

    print(
        f'Small deep GraphQL queries averaged at: '
        f'{round(1000 * gql_deep_total/num_runs, 2)} ms'
    )
    print(
        f'Small shallow GraphQL queries averaged at: '
        f'{round(1000 * gql_shallow_total/num_runs, 2)} ms'
    )
    print(
        f'Small DRF queries averaged at: '
        f'{round(1000 * drf_total/num_runs, 2)} ms'
    )
    print(
        f'Small DRF queries related averaged at: '
        f'{round(1000 * drf_related_total/num_runs, 2)} ms'
    )
    print('------------------------------')

    gql_shallow_total = 0
    gql_deep_total = 0
    drf_total = 0
    drf_related_total = 0

    for i in range(num_runs):
        time = performance_tester(num_addresses=100)
        drf_total += time['drf_time']
        gql_shallow_total += time['gql_shallow_time']
        gql_deep_total += time['gql_deep_time']
        drf_related_total += time['drf_related_time']

    print(
        f'Large deep GraphQL queries averaged at: '
        f'{round(1000 * gql_deep_total/num_runs, 2)} ms'
    )
    print(
        f'Large shallow GraphQL queries averaged at: '
        f'{round(1000 * gql_shallow_total/num_runs, 2)} ms'
    )
    print(
        f'Large DRF queries averaged at: '
        f'{round(1000 * drf_total/num_runs, 2)} ms'
    )
    print(
        f'Large DRF queries related averaged at: '
        f'{round(1000 * drf_related_total/num_runs, 2)} ms'
    )
    print('------------------------------')

    assert False  # Print results
