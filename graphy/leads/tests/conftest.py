import pytest

from graphy.leads.models import Lead


@pytest.fixture
def lead(db):
    return Lead.objects.create(
        email='tomfa@otovo.com',
        address=None,
        uncleaned_address='Parkveien 4b, 0350 Oslo',
        utm_campaign='kolonial_graphene_talk',
        utm_medium='shell',
        utm_source='presentation',
    )
