from django.db import models

from graphy.location.models import Address
from graphy.utils.base_models import BaseModel


class Lead(BaseModel):
    email = models.EmailField(
        help_text='Email left by user, where an offer may be sent.'
    )
    address = models.ForeignKey(
        Address,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text=(
            'Cleaned and verified address where user is interested in solar '
            'panels.'
        ),
    )
    uncleaned_address = models.CharField(
        max_length=64,
        help_text="Uncleaned input of the address that wants solar panels",
    )

    utm_campaign = models.CharField(max_length=64, help_text='Campaign, e.g. BlackFriday2018')
    utm_medium = models.CharField(max_length=64, help_text='Advertising medium, e.g. email, Banner Ad or Pay per Click Ads')
    utm_source = models.CharField(max_length=64, help_text='Channel, e.g. Google, Facebook')
