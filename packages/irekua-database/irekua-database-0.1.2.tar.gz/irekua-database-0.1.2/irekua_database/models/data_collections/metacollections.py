from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models import base


class MetaCollection(base.IrekuaModelBaseUser):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of meta collection'),
        null=False,
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of Meta Collection'),
        blank=False)

    items = models.ManyToManyField(
        'Item',
        verbose_name=_('items'),
        help_text=_('Items belonging to MetaCollection'),
        blank=True)
    curators = models.ManyToManyField(
        'User',
        related_name='metacollection_curators',
        verbose_name='curators',
        help_text=_('Curators of metacollection'),
        blank=True)

    class Meta:
        verbose_name = _('Meta Collection')
        verbose_name_plural = _('Meta Collections')

        ordering = ['name']

    def __str__(self):
        return self.name

    def add_item(self, item):
        self.items.add(item)  # pylint: disable=E1101
        self.save()

    def remove_item(self, item):
        self.items.remove(item)  # pylint: disable=E1101
        self.save()

    def add_curator(self, user):
        self.curators.add(user)  # pylint: disable=E1101
        self.save()

    def remove_curator(self, user):
        self.curators.remove(user)  # pylint: disable=E1101
        self.save()
