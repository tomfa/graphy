from rest_framework.routers import DefaultRouter

from graphy.leads.views import CountyAPIViewSet


app_name = 'location'

router = DefaultRouter()
router.register(r'counties', CountyAPIViewSet, basename='counties')

urlpatterns = router.urls
