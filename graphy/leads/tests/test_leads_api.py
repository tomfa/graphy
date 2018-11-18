from rest_framework import status

from graphy.leads.models import Lead
from graphy.leads.serializers import LeadSerializer


def test_empty_lead_list(drf_client):
    response = drf_client.get('/leads/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_lead_list(drf_client, lead):
    response = drf_client.get('/leads/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [LeadSerializer(instance=lead).data]


def test_lead_create(drf_client):
    assert Lead.objects.count() == 0

    response = drf_client.post(
        '/leads/',
        {'address': 'Parkveien 4b, 0350 Oslo', 'email': 'me@example.com'},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        'address': None,
        'email': 'me@example.com',
        'utm_campaign': '',
        'utm_medium': '',
        'utm_source': '',
    }
    assert Lead.objects.count() == 1
