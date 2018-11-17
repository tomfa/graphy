import pytest

from rest_framework import test


@pytest.fixture
def client(db):
    return test.APIClient()
