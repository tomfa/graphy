from graphene.test import Client as GraphQLClient

import pytest

from rest_framework import test

from graphy.schema import schema


@pytest.fixture
def drf_client(db):
    return test.APIClient()


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
