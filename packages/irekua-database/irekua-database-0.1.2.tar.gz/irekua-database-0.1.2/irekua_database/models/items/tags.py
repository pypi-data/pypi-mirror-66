from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models import base


class Tag(base.IrekuaModelBase):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of tag'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Tag description'),
        blank=True)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Icon for tag'),
        upload_to='images/tags/',
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

        ordering = ['name']

    def __str__(self):
        return self.name
