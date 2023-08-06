from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import base


class CollectionRole(base.IrekuaModelBase):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which role applies'),
        blank=False,
        null=False)
    role = models.ForeignKey(
        'Role',
        on_delete=models.PROTECT,
        db_column='role_id',
        verbose_name=_('role'),
        help_text=_('Role to be part of collection'),
        blank=False,
        null=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of collection role info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Collection Role')
        verbose_name_plural = _('Collection Roles')

        unique_together = (
            ('collection_type', 'role'),
        )

    def __str__(self):
        msg = _('Role %(role)s for collections of type %(collection)s')
        params = dict(
            role=str(self.role),
            collection=str(self.collection_type))
        return msg % params

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _(
                'Invalid metadata for user of role type %(type)s '
                'in collection %(collection)s. Error: %(error)s')
            params = dict(
                type=str(self.role),
                collection=str(self.collection_type),
                error=str(error))
            raise ValidationError(msg, params=params)
