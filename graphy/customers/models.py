from django.contrib.auth import get_user_model
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from graphy.location.models import Address
from graphy.utils.base_models import BaseModel


class Customer(BaseModel):
    email = models.EmailField(help_text='Email where we may reach customer.')
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        help_text="Prefix with +46 for Sweden and +47 for Norway.",
    )
    user = models.OneToOneField(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Connected user for the customer.",
    )
    home_address = models.ForeignKey(
        Address,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="The home address of the customer.",
    )
