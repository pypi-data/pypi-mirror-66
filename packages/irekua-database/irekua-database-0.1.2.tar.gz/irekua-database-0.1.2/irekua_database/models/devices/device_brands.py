from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models import base


class DeviceBrand(base.IrekuaModelBase):
    name = models.CharField(
        max_length=128,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of device brand'),
        unique=True,
        blank=False)
    website = models.URLField(
        db_column='website',
        verbose_name=_('website'),
        help_text=_('Brand\'s website'),
        blank=True,
        null=True)
    logo = models.ImageField(
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Logo of device brand'),
        upload_to='images/device_brands/',
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Device Brand')
        verbose_name_plural = _('Device Brands')

        ordering = ['name']

    def __str__(self):
        return self.name
