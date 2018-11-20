from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from graphy.utils.graphql import AuthenticatedGraphQLView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('location/', include('graphy.location.urls')),
    path('leads/', include('graphy.leads.urls')),
    path('customers/', include('graphy.customers.urls')),
    path(
        'graphql/', AuthenticatedGraphQLView.as_view(graphiql=settings.DEBUG)
    ),
]
