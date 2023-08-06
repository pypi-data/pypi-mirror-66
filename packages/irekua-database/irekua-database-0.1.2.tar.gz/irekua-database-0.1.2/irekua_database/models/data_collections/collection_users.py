from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class CollectionUser(base.IrekuaModelBaseUser):
    collection = models.ForeignKey(
        'Collection',
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which user belongs'),
        on_delete=models.CASCADE,
        blank=False)
    user = models.ForeignKey(
        'User',
        db_column='user_id',
        verbose_name=_('user'),
        help_text=_('User of collection'),
        on_delete=models.CASCADE,
        blank=False)
    role = models.ForeignKey(
        'Role',
        on_delete=models.PROTECT,
        db_column='role_id',
        verbose_name=_('role'),
        help_text=_('Role of user in collection'),
        blank=False)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        verbose_name=_('metadata'),
        default=empty_JSON,
        help_text=_('Metadata associated to user in collection'),
        null=True)

    class Meta:
        verbose_name = _('Collection User')
        verbose_name_plural = _('Collection Users')

        unique_together = (
            ('collection', 'user'),
        )

    def __str__(self):
        msg = _('%(user)s (%(role)s)')
        params = dict(
            user=str(self.user),
            role=str(self.role))
        return msg % params

    def clean(self):
        try:
            collection_role = self.collection.validate_and_get_role(self.role)
        except ValidationError:
            msg = _("Role is not valid for this collection's type")
            raise ValidationError({'role': msg})

        try:
            collection_role.validate_metadata(self.metadata)
        except ValidationError as error:
            msg = _(
                'Invalid metadata for user of role type %(role)s '
                'in collection %(collection)s. Error: %(error)s')
            params = dict(
                role=str(self.role),
                collection=str(self.collection),
                error=str(error))
            raise ValidationError({'metadata': msg}, params=params)
        super().clean()
