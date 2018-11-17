from rest_framework.routers import DefaultRouter

from graphy.location.views import (
    AddressAPIViewSet,
    CountyAPIViewSet,
    ZipCodeAPIViewSet,
)


app_name = 'location'

router = DefaultRouter()

router.register(r'addresses', AddressAPIViewSet, basename='addresses')
router.register(r'counties', CountyAPIViewSet, basename='counties')
router.register(r'zipcodes', ZipCodeAPIViewSet, basename='zipcodes')

urlpatterns = router.urls
