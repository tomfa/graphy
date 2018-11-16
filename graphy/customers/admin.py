from django.contrib import admin

from graphy.customers.models import Customer
from graphy.utils.base_models import BaseAdmin


@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    list_display = ('email', 'home_address')
    fields = (
        'email',
        'phone_number',
    )
    raw_id_fields = ('home_address', 'user',)
