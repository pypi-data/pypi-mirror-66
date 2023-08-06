from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base
from irekua_database.models.items.items import Item
from irekua_database.models.sampling_events.sampling_event_devices import SamplingEventDevice


class PhysicalDevice(base.IrekuaModelBaseUser):
    identifier = models.CharField(
        max_length=128,
        db_column='identifier',
        verbose_name=_('name'),
        help_text=_('Simple device identifier (visible only to owner)'),
        blank=True,
    )
    serial_number = models.CharField(
        max_length=128,
        db_column='serial_number',
        verbose_name=_('serial number'),
        help_text=_('Serial number of device'),
        blank=True,
        null=True)
    device = models.ForeignKey(
        'Device',
        on_delete=models.PROTECT,
        db_column='device_id',
        verbose_name=_('device'),
        help_text=_('Brand and model of device'),
        blank=False,
        null=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to device'),
        default=empty_JSON,
        null=True,
        blank=True)
    bundle = models.BooleanField(
        db_column='bundle',
        verbose_name=_('bundle'),
        help_text=_(
            'Does this device possibly represents many '
            'physical devices?'),
        blank=False)

    class Meta:
        verbose_name = _('Physical Device')
        verbose_name_plural = _('Physical Devices')
        unique_together = (
            ('serial_number', 'device'),
        )

        ordering = ['-created_on']

    def __str__(self):
        if self.identifier:
            return self.identifier

        msg = _('Device %(id)s of type %(device)s')
        params = dict(
            id=self.id,
            device=str(self.device))
        return msg % params

    def clean(self):
        try:
            self.device.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        super(PhysicalDevice, self).clean()

    @cached_property
    def items(self):
        return Item.objects.filter(
            sampling_event_device__collection_device__physical_device=self)

    @cached_property
    def sampling_events(self):
        return SamplingEventDevice.objects.filter(
            collection_device__physical_device=self)

    @cached_property
    def deployments(self):
        return SamplingEventDevice.objects.filter(
            collection_device__physical_device=self)

    def validate_configuration(self, configuration):
        self.device.validate_configuration(configuration)
