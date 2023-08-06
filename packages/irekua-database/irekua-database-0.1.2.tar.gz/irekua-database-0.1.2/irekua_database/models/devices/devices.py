from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import JSONField

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import base


class Device(base.IrekuaModelBase):
    device_type = models.ForeignKey(
        'DeviceType',
        on_delete=models.PROTECT,
        related_name='device_type',
        db_column='device_type_id',
        verbose_name=_('device type'),
        help_text=_('Type of device'),
        blank=False)
    brand = models.ForeignKey(
        'DeviceBrand',
        on_delete=models.PROTECT,
        related_name='device_brand',
        db_column='device_brand_id',
        verbose_name=_('brand'),
        help_text=_('Brand of device'),
        blank=False)
    model = models.CharField(
        max_length=64,
        db_column='model',
        verbose_name=_('model'),
        help_text=_('Model of device'),
        blank=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of device info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])
    configuration_schema = JSONField(
        db_column='configuration_schema',
        verbose_name=_('configuration schema'),
        help_text=_('JSON Schema for configuration info of device'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        unique_together = (('brand', 'model'))

        ordering = ['brand', 'model']

    def __str__(self):
        msg = '%(device_type)s: %(brand)s - %(model)s'
        params = dict(
            device_type=self.device_type,
            brand=self.brand,
            model=self.model)
        return msg % params

    def validate_configuration(self, configuration):
        try:
            validate_JSON_instance(
                schema=self.configuration_schema,
                instance=configuration)
        except ValidationError as error:
            msg = _('Invalid device configuration. Error: %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _('Invalid device metadata. Error: %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)
