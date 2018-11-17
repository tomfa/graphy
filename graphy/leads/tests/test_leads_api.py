from rest_framework import status

from graphy.leads.serializers import LeadSerializer


def test_empty_lead_list(client):
    response = client.get('/leads/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_lead_list(client, lead):
    response = client.get('/leads/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        LeadSerializer(instance=lead).data
    ]
