from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.models.items.items import Item
from irekua_database.utils import empty_JSON
from irekua_database.models import base


class CollectionDevice(base.IrekuaModelBaseUser):
    physical_device = models.ForeignKey(
        'PhysicalDevice',
        on_delete=models.PROTECT,
        db_column='physical_device_id',
        verbose_name=_('physical device'),
        help_text=_('Reference to physical device'),
        blank=False,
        null=False)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which the device belongs'),
        blank=False,
        null=False)
    internal_id = models.CharField(
        max_length=64,
        db_column='internal_id',
        verbose_name=_('ID within collection'),
        help_text=_('ID of device within the collection (visible to all collection users)'),
        blank=True)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        default=empty_JSON,
        verbose_name=_('metadata'),
        help_text=_('Metadata associated with device within collection'),
        null=True)

    class Meta:
        verbose_name = _('Collection Device')
        verbose_name_plural = _('Collection Devices')

        ordering = ['-modified_on']

        unique_together = (
            ('physical_device', 'collection'),
        )

    def __str__(self):
        if self.internal_id:
            return self.internal_id
        return _('Collection device {}').format(self.id)

    def clean(self):
        try:
            device_type = self.collection.validate_and_get_device_type(
                self.physical_device.device.device_type)
        except ValidationError as error:
            raise ValidationError({'physical_device': error})

        if device_type is not None:
            try:
                device_type.validate_metadata(self.metadata)
            except ValidationError as error:
                raise ValidationError({'metadata': str(error)})

        super(CollectionDevice, self).clean()

    @property
    def items(self):
        queryset = Item.objects.filter(sampling_event_device__collection_device=self)
        return queryset
