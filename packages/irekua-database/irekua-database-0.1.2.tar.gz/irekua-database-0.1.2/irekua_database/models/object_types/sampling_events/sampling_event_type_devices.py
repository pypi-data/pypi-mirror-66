from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import base


class SamplingEventTypeDeviceType(base.IrekuaModelBase):
    sampling_event_type = models.ForeignKey(
        'SamplingEventType',
        on_delete=models.CASCADE,
        db_column='sampling_event_type_id',
        verbose_name=_('sampling event type'),
        help_text=_(
            'Sampling event type in which this device '
            'types can be placed'),
        null=False,
        blank=False)
    device_type = models.ForeignKey(
        'DeviceType',
        on_delete=models.PROTECT,
        db_column='device_type_id',
        verbose_name=_('device type'),
        help_text=_(
            'Type of device that can be used in sampling '
            'event of the given type'),
        null=False,
        blank=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_(
            'JSON schema for metadata associated to device '
            'in sampling event'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Sampling Event Type Device Type')
        verbose_name_plural = _('Sampling Event Type Device Types')

        ordering = ['sampling_event_type']
        unique_together = (
            ('sampling_event_type', 'device_type'),
        )

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _(
                'Invalid metadata for device of type %(device)s in sampling'
                'event of type %(sampling_event)s. Error: %(error)')
            params = dict(
                device=str(self.device_type),
                sampling_event=str(self.sampling_event_type),
                error=str(error))
            raise ValidationError(msg, params=params)
