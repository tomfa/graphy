from graphy.location.serializers import AddressSerializer


def test_address_serializer(address):
    assert AddressSerializer(instance=address).data == {
        'id': str(address.id),
        'street_address': 'Parkveien 4b',
        'country': 'no',
        'latitude': '59.9217031000000',
        'longitude': '10.7285179000000',
        'zip_code': {
            'id': str(address.zip_code.id),
            'code': '0350',
            'name': 'Oslo',
            'municipality': {
                'id': str(address.zip_code.municipality.id),
                'name': 'Oslo',
                'county': {
                    'id': str(address.zip_code.municipality.county.id),
                    'code': '03',
                    'name': 'Oslo',
                    'country': 'no',
                },
            },
            'county': {
                'id': str(address.zip_code.county.id),
                'code': '03',
                'name': 'Oslo',
                'country': 'no',
            },
        },
    }
