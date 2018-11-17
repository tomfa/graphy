from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('location/', include('graphy.location.urls')),
    path('leads/', include('graphy.leads.urls')),
]
