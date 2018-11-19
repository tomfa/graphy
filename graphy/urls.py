from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from graphene_django.views import GraphQLView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('location/', include('graphy.location.urls')),
    path('leads/', include('graphy.leads.urls')),
    path('customers/', include('graphy.customers.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=settings.DEBUG)),
]
