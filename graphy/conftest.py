from django.contrib.auth import get_user_model

from graphene.test import Client as GraphQLClient

import pytest

from rest_framework import test

from graphy.schema import schema


@pytest.fixture
def user(db):
    return get_user_model().objects.create(
        username='zaphod@example.com',
        email='zaphod@example.com',
        first_name='Zaphod',
        last_name='Beeblebrox',
    )


@pytest.fixture
def staff_user(db):
    return get_user_model().objects.create(
        username='marvin@example.com',
        email='marvin@example.com',
        first_name='Marvin',
        is_staff=True,
    )


@pytest.fixture
def drf_client(db):
    return test.APIClient()


@pytest.fixture()
def drf_client_staff(drf_client, staff_user):
    drf_client.force_login(user=staff_user)
    return drf_client


@pytest.fixture()
def drf_client_user(drf_client, user):
    drf_client.force_login(user=user)
    return drf_client


@pytest.fixture
def gql_client():
    class Request:
        def __init__(self):
            self.META = {}

    class Context:
        def __init__(self):
            self._request = Request()
            self.META = {}

    return GraphQLClient(schema, context=Context())
