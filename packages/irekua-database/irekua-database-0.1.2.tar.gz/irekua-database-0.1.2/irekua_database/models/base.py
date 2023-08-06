from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models.users import users


class IrekuaModelBase(models.Model):
    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of creation'),
        editable=False,
        auto_now_add=True)
    modified_on = models.DateTimeField(
        db_column='modified_on',
        verbose_name=_('modified on'),
        help_text=_('Date of last modification'),
        editable=False,
        auto_now=True)

    class Meta:
        abstract = True


class IrekuaModelBaseUser(IrekuaModelBase):
    created_by = models.ForeignKey(
        users.User,
        on_delete=models.PROTECT,
        db_column='creator_id',
        related_name='%(class)s_created_by',
        verbose_name=_('creator'),
        blank=True,
        null=True,
        help_text=_('Creator of object'))
    modified_by = models.ForeignKey(
        users.User,
        db_column='modified_by',
        on_delete=models.SET_NULL,
        editable=False,
        related_name='%(class)s_modified_by',
        verbose_name=_('modified by'),
        help_text=_('User who made modifications last'),
        blank=True,
        null=True)

    class Meta:
        abstract = True
