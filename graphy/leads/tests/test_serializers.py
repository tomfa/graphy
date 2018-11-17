from graphy.leads.serializers import LeadSerializer


def test_lead_serializer(lead):
    assert LeadSerializer(instance=lead).data == {
        'id': str(lead.id),
        'email': 'tomfa@otovo.com',
        'address': None,
        'uncleaned_address': 'Parkveien 4b, 0350 Oslo',
        'utm_campaign': 'kolonial_graphene_talk',
        'utm_medium': 'shell',
        'utm_source': 'presentation',
    }
