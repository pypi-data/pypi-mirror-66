from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import base


class CollectionItemType(base.IrekuaModelBase):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which role applies'),
        blank=False,
        null=False)
    item_type = models.ForeignKey(
        'ItemType',
        on_delete=models.PROTECT,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Item to be part of collection'),
        blank=False,
        null=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of collection item info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Collection Item Type')
        verbose_name_plural = _('Collection Item Types')

        unique_together = (
            ('collection_type', 'item_type'),
        )

    def __str__(self):
        msg = _('Item type %(item)s for collection %(collection)s')
        params = dict(
            item=str(self.item_type),
            collection=str(self.collection_type))
        return msg % params

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _(
                'Invalid metadata for item type %(type)s in collection '
                '%(collection). Error: %(error)')
            params = dict(
                type=str(self.item_type),
                collection_type=str(self.collection_type),
                error=str(error))
            raise ValidationError(msg, params=params)
