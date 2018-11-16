from django.contrib import admin

from graphy.location.models import County, Address, ZipCode, Municipality
from graphy.utils.base_models import BaseAdmin


@admin.register(County)
class CountyAdmin(BaseAdmin):
    list_display = ('name', 'code', 'country')


@admin.register(Municipality)
class MunicipalityAdmin(BaseAdmin):
    list_display = ('name', 'county')
    list_filter = ('county',)
    raw_id_fields = ('county',)


@admin.register(ZipCode)
class ZipCodeAdmin(BaseAdmin):
    list_display = ('name', 'code', 'county')
    list_filter = ('county',)
    fields = ('code', 'name', 'municipality', 'county')
    raw_id_fields = ('municipality', 'county')


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    list_display = ('street_address', 'zip_code', 'country')
    fields = ('street_address', 'zip_code', 'country', 'latitude', 'longitude')

    raw_id_fields = ('zip_code',)
