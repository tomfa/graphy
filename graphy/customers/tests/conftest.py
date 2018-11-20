import pytest

from graphy.customers.models import Customer
from graphy.location.tests.conftest import *  # noqa


@pytest.fixture
def customer(address):
    return Customer.objects.create(
        email='fishsticks@example.com',
        phone_number='+4741231234',
        home_address=address
    )


@pytest.fixture
def customer_with_user(user, address):
    return Customer.objects.create(
        email='cake@example.com',
        phone_number='+4741231234',
        home_address=address,
        user=user,
    )
