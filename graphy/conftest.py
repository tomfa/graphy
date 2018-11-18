import pytest

from rest_framework import test


@pytest.fixture
def drf_client(db):
    return test.APIClient()
