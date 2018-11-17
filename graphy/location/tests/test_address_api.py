from rest_framework import status

from graphy.location.serializers import AddressSerializer


def test_empty_address_list(client):
    response = client.get('/location/addresses/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_address_list(client, address):
    response = client.get('/location/addresses/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        AddressSerializer(instance=address).data
    ]
