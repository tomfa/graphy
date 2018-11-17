from decimal import Decimal

import pytest

from rest_framework import test

from graphy.location.enums import Country
from graphy.location.models import Address, County, Municipality, ZipCode


@pytest.fixture
def client(db):
    return test.APIClient()


@pytest.fixture
def country():
    return Country.NO


@pytest.fixture
def county(db, country):
    return County.objects.create(country=country, code='03', name='Oslo')


@pytest.fixture
def municipality(county):
    return Municipality.objects.create(name='Oslo', county=county)


@pytest.fixture
def zip_code(municipality, county):
    return ZipCode.objects.create(
        code='0350', name='Oslo', municipality=municipality, county=county
    )


@pytest.fixture
def address(db, zip_code, country):
    return Address.objects.create(
        street_address="Parkveien 4b",
        zip_code=zip_code,
        country=country,
        latitude=Decimal(59.9217031),
        longitude=Decimal(10.7285179),
    )
