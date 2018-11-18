from graphy.location.tests.conftest import *  # noqa


def test_lead_type(gql_client, lead, address):
    lead.address = address
    lead.save()
    query = """
        query($id: UUID!) {
          lead(id: $id) {
            id
            email
            address {
              id
            }
            uncleanedAddress
            utmCampaign
            utmMedium
            utmSource
          }
        }
    """
    params = {'id': str(lead.id)}

    result = gql_client.execute(query, variables=params)

    lead_dict = result['data']['lead']
    assert lead_dict == {
        'id': str(lead.id),
        'email': lead.email,
        'address': {'id': str(lead.address.id)},
        'uncleanedAddress': lead.uncleaned_address,
        'utmCampaign': lead.utm_campaign,
        'utmMedium': lead.utm_medium,
        'utmSource': lead.utm_source,
    }
