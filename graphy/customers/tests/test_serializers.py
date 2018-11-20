from graphy.customers.serializers import CustomerSerializer


def test_customer_serializer(customer):
    assert CustomerSerializer(instance=customer).data == {
        'id': str(customer.id),
        'email': 'fishsticks@example.com',
        'phone_number': '+4741231234',
        'user': None,
        'leads': [],
    }
