from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON

from irekua_database.models.items.items import Item
from irekua_database.models.sampling_events.sampling_event_devices import SamplingEventDevice
from irekua_database.models import base


class CollectionSite(base.IrekuaModelBaseUser):
    site_type = models.ForeignKey(
        'SiteType',
        on_delete=models.PROTECT,
        db_column='site_type',
        verbose_name=_('site type'),
        help_text=_('Type of site'),
        blank=False,
        null=False)
    site = models.ForeignKey(
        'Site',
        on_delete=models.PROTECT,
        db_column='site_id',
        verbose_name=_('site'),
        help_text=_('Reference to Site'),
        blank=False,
        null=False)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which the site belongs'),
        blank=False,
        null=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to site in collection'),
        default=empty_JSON,
        blank=True,
        null=True)
    internal_id = models.CharField(
        max_length=64,
        db_column='internal_id',
        verbose_name=_('ID within collection'),
        help_text=_('ID of site within the collection (visible to all collection users)'),
        blank=True)

    site_descriptors = models.ManyToManyField(
        'SiteDescriptor',
        blank=True)

    class Meta:
        verbose_name = _('Collection Site')
        verbose_name_plural = _('Collection Sites')

        unique_together = (
            ('collection', 'site'),
            ('collection', 'internal_id'),
        )

    def __str__(self):
        if self.internal_id:
            return self.internal_id

        if self.site.name:
            return self.site.name

        msg = _('Site %(id)s')
        params = dict(id=str(self.id))
        return msg % params

    def clean(self):
        try:
            self.collection.validate_and_get_site_type(self.site_type)
        except ValidationError as error:
            raise ValidationError({'site': error})

        super(CollectionSite, self).clean()

    def add_descriptor(self, descriptor):
        self.site_type.validate_descriptor_type(descriptor)
        self.site_descriptors.add(descriptor)

    def remove_descriptor(self, descriptor):
        self.site_descriptors.remove(descriptor)

    @property
    def items(self):
        queryset = Item.objects.filter(
            sampling_event_device__sampling_event__collection_site=self)
        return queryset

    @cached_property
    def deployments(self):
        return SamplingEventDevice.objects.filter(sampling_event__collection_site=self)
