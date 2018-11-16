from django.contrib import admin

from graphy.leads.models import Lead
from graphy.utils.base_models import BaseAdmin


@admin.register(Lead)
class LeadAdmin(BaseAdmin):
    list_display = ('uncleaned_address', 'email')
    fields = (
        'email',
        'address',
        'uncleaned_address',
        'utm_campaign',
        'utm_medium',
        'utm_source',
    )
    raw_id_fields = ('address',)
