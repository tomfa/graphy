from rest_framework.routers import DefaultRouter

from graphy.customers.views import CustomerViewSet


app_name = 'customers'

router = DefaultRouter()

router.register('', CustomerViewSet, basename='customers')

urlpatterns = router.urls
