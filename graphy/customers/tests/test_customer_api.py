from rest_framework import status


def test_list_as_anonymous(drf_client, customer, customer_with_user):
    response = drf_client.get('/customers/')

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_as_customer(drf_client_user, customer, customer_with_user):
    response = drf_client_user.get('/customers/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
            'id': str(customer_with_user.id),
            'email': 'cake@example.com',
            'phone_number': '+4741231234',
            'user': {
                'id': customer_with_user.user.id,
                'username': 'zaphod@example.com',
                'email': 'zaphod@example.com',
                'first_name': 'Zaphod',
                'last_name': 'Beeblebrox',
                'full_name': 'Zaphod Beeblebrox',
                'is_staff': False,
            },
            'leads': [],
        }
    ]


def test_list_as_staff(drf_client_staff, customer, customer_with_user):
    response = drf_client_staff.get('/customers/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
            'id': str(customer.id),
            'email': 'fishsticks@example.com',
            'phone_number': '+4741231234',
            'user': None,
            'leads': [],
        },
        {
            'id': str(customer_with_user.id),
            'email': 'cake@example.com',
            'phone_number': '+4741231234',
            'user': {
                'id': customer_with_user.user.id,
                'username': 'zaphod@example.com',
                'email': 'zaphod@example.com',
                'first_name': 'Zaphod',
                'last_name': 'Beeblebrox',
                'full_name': 'Zaphod Beeblebrox',
                'is_staff': False,
            },
            'leads': [],
        },
    ]


def test_get_as_anonymous(drf_client, customer_with_user):
    response = drf_client.get(f'/customers/{customer_with_user.id}/')

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_as_customer(drf_client_user, customer_with_user):
    response = drf_client_user.get(f'/customers/{customer_with_user.id}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'id': str(customer_with_user.id),
        'email': 'cake@example.com',
        'phone_number': '+4741231234',
        'user': {
            'id': customer_with_user.user.id,
            'username': 'zaphod@example.com',
            'email': 'zaphod@example.com',
            'first_name': 'Zaphod',
            'last_name': 'Beeblebrox',
            'full_name': 'Zaphod Beeblebrox',
            'is_staff': False,
        },
        'leads': [],
    }


def test_get_as_staff(drf_client_staff, customer_with_user):
    response = drf_client_staff.get(f'/customers/{customer_with_user.id}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'id': str(customer_with_user.id),
        'email': 'cake@example.com',
        'phone_number': '+4741231234',
        'user': {
            'id': customer_with_user.user.id,
            'username': 'zaphod@example.com',
            'email': 'zaphod@example.com',
            'first_name': 'Zaphod',
            'last_name': 'Beeblebrox',
            'full_name': 'Zaphod Beeblebrox',
            'is_staff': False,
        },
        'leads': [],
    }
