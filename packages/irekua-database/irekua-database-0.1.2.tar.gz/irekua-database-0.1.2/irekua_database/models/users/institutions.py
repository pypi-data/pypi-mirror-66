from django.db import models
from django.utils.translation import gettext_lazy as _
import pycountry

from irekua_database.models import base


class Institution(base.IrekuaModelBaseUser):
    COUNTRIES = (
        (country.alpha_2, country.name) for country in pycountry.countries
    )

    institution_name = models.CharField(
        max_length=256,
        db_column='institution_name',
        verbose_name=_('institution name'),
        help_text=_('Name of institution'),
        blank=False)
    institution_code = models.CharField(
        max_length=64,
        db_column='institution_code',
        verbose_name=_('institution code'),
        help_text=_('Code of institution'),
        blank=True)
    subdependency = models.CharField(
        max_length=256,
        db_column='subdependency',
        verbose_name=_('subdependency'),
        help_text=_('Subdependency at institution'),
        blank=True,
        null=True)
    country = models.CharField(
        max_length=2,
        choices=COUNTRIES,
        db_column='country',
        verbose_name=_('country'),
        help_text=_('Country home of institution'),
        blank=True)
    postal_code = models.CharField(
        max_length=8,
        db_column='postal_code',
        verbose_name=_('postal code'),
        help_text=_('Postal code'),
        blank=True)
    address = models.TextField(
        blank=True,
        db_column='address',
        verbose_name=_('address'),
        help_text=_('Address of institution'))
    website = models.URLField(
        blank=True,
        db_column='website',
        verbose_name=_('website'),
        help_text=_('Website of institution'))
    logo = models.ImageField(
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Institution logo'),
        upload_to='images/institutions/',
        blank=True,
        null=True)

    class Meta:
        ordering = ['institution_name']
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')
        unique_together = (('institution_name', 'subdependency'))

    def __str__(self):
        name = self.institution_code
        if name is None or name == '':
            name = self.institution_name

        if self.subdependency is not None and self.subdependency != '':
            name += ' - ' + self.subdependency
        return name

    def has_user(self, user):
        queryset = self.user_set.filter(id=user.id)
        return queryset.exists()
