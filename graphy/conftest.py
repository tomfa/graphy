from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from graphene.test import Client as GraphQLClient

import pytest

from rest_framework import test

from graphy.schema import schema
from graphy.utils.graphql import AuthenticatedGraphQLView


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
            self.user = AnonymousUser()
            self._request = Request()
            self.META = {}

    return GraphQLClient(
        schema,
        format_error=AuthenticatedGraphQLView.format_error,
        context=Context(),
    )


@pytest.fixture
def gql_client_staff(staff_user):
    class Request:
        def __init__(self):
            self.META = {}

    class Context:
        def __init__(self, user):
            self.user = user
            self._request = Request()
            self.META = {}

    return GraphQLClient(
        schema,
        format_error=AuthenticatedGraphQLView.format_error,
        context=Context(user=staff_user),
    )


@pytest.fixture
def gql_client_user(user):
    class Request:
        def __init__(self):
            self.META = {}

    class Context:
        def __init__(self, user):
            self.user = user
            self._request = Request()
            self.META = {}

    return GraphQLClient(
        schema,
        format_error=AuthenticatedGraphQLView.format_error,
        context=Context(user=user),
    )
