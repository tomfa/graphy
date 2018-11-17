from rest_framework.routers import DefaultRouter

from graphy.leads.views import LeadAPIViewSet


app_name = 'leads'

router = DefaultRouter()

router.register('', LeadAPIViewSet, basename='leads')

urlpatterns = router.urls
