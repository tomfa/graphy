from rest_framework import status

from graphy.location.serializers import AddressSerializer


def test_empty_address_list(drf_client):
    response = drf_client.get('/location/addresses/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_address_list(drf_client, address):
    response = drf_client.get('/location/addresses/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        AddressSerializer(instance=address).data
    ]
