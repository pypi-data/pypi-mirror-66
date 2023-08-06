from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import base


class CollectionDeviceType(base.IrekuaModelBase):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which role applies'),
        blank=False,
        null=False)
    device_type = models.ForeignKey(
        'DeviceType',
        on_delete=models.PROTECT,
        db_column='device_type_id',
        verbose_name=_('device type'),
        help_text=_('Device to be part of collection'),
        blank=False,
        null=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of collection device info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Collection Device Type')
        verbose_name_plural = _('Collection Device Types')

        unique_together = (
            ('collection_type', 'device_type'),
        )

    def __str__(self):
        msg = _(
            'Device type %(device_type)s for collection '
            'type %(collection_type)s')
        params = dict(
            device_type=str(self.device_type),
            collection_type=str(self.collection_type))
        return msg % params

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for collection device. Error: %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)
