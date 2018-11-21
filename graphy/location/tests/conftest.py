from decimal import Decimal
import time

from django.db import connection
from django.test.utils import CaptureQueriesContext
import pytest

from rest_framework import test

from graphy.location.enums import Country
from graphy.location.models import Address, County, Municipality, ZipCode


def queries(fun):
    with CaptureQueriesContext(connection) as context:
        fun()
        return list(q['sql'] for q in context.captured_queries)


def timing(f):
    time1 = time.time()
    f()
    time2 = time.time()

    return time2 - time1


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
