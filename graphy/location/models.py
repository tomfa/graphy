from django.core import validators
from django.db import models

from graphy.utils.base_models import BaseModel


class County(BaseModel):
    code = models.CharField(
        max_length=2,
        validators=[validators.RegexValidator(regex=r'^\d{2}$')], help_text='National 2-digit identifier of County.')
    name = models.CharField(max_length=50)


class Municipality(BaseModel):
    name = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.CASCADE)


class ZipCode(BaseModel):
    code = models.CharField(
        max_length=5,
        validators=[validators.RegexValidator(regex=r'^\d{4,5}$')])
    name = models.CharField(max_length=50, help_text='Postal name of zip code')
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        unique_together = ('code', 'county')
        ordering = ('code',)


class Address(BaseModel):
    street_address = models.CharField(max_length=254, blank=True)
    zip_code = models.ForeignKey(
        ZipCode, on_delete=models.PROTECT, null=True, blank=True)

    latitude = models.DecimalField(
        max_digits=15, decimal_places=13, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=16, decimal_places=13, null=True, blank=True)
