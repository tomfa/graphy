from django.db import connection
from django.test.utils import CaptureQueriesContext


def queries(fun):
    with CaptureQueriesContext(connection) as context:
        fun()
        return list(q['sql'] for q in context.captured_queries)


def test_drf_without_select_related_uses_5_calls(drf_client, address):
    # DRF will run query in get_queryset.
    sqls = queries(
        lambda: drf_client.get(f'/location/addresses/{address.id}/')
    )
    assert len(sqls) == 5


def test_drf_with_select_related_uses_1_call(drf_client, address):
    # DRF will run query in get_queryset.
    sqls = queries(
        lambda: drf_client.get(
            f'/location/addresses/{address.id}/?select_related'
        )
    )
    assert len(sqls) == 1


def test_gql_select_everything_uses_5_calls(gql_client, address):
    query = """
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
    sqls = queries(
        lambda: gql_client.execute(query)
    )
    assert len(sqls) == 5


def test_graphene_fetches_whole_db_object(gql_client, address):
    # Query only requires one field. Graphene will ask for whole object
    query = """
        query($id: UUID!) {
          address(id: $id) {
            id
          }
        }
    """
    params = {'id': str(address.id)}

    sqls = queries(lambda: gql_client.execute(query, variables=params))

    assert len(sqls) == 1
    assert sqls[0].startswith(
        'SELECT "location_address"."id", '
        '"location_address"."created_at", '
        '"location_address"."updated_at", '
        '"location_address"."street_address", '
        '"location_address"."zip_code_id", '
        '"location_address"."country", '
        '"location_address"."latitude", '
        '"location_address"."longitude" FROM '
    )


def test_graphene_does_not_utilize_select_related(gql_client, address):
    # Graphene will not attempt to use .select- or .prefetch_related.
    query = """
        query($id: UUID!) {
          address(id: $id) {
            id
            country
            streetAddress
            latitude
            longitude
            zipCode {
              id
              code
              name
            }
          }
        }
    """
    params = {'id': str(address.id)}

    sqls = queries(lambda: gql_client.execute(query, variables=params))
    assert len(sqls) == 2


def test_graphene_fethes_fk_object_even_if_we_only_need_id(
    gql_client, address
):
    # zipCode.id is available on address.zip_code_id, so 1 query is sufficient.
    # Graphene will still do an extra call for retrieving zip code instance.
    query = """
        query($id: UUID!) {
          address(id: $id) {
            id
            zipCode {
              id
            }
          }
        }
    """
    params = {'id': str(address.id)}

    sqls = queries(lambda: gql_client.execute(query, variables=params))
    assert len(sqls) == 2
