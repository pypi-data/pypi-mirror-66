from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base
from irekua_database.models import Item


class SamplingEvent(base.IrekuaModelBaseUser):
    sampling_event_type = models.ForeignKey(
        'SamplingEventType',
        on_delete=models.PROTECT,
        db_column='sampling_event_type',
        verbose_name=_('sampling event type'),
        help_text=_('Type of sampling event'),
        blank=False,
        null=False)
    collection_site = models.ForeignKey(
        'CollectionSite',
        db_column='collection_site_id',
        verbose_name=_('collection site'),
        help_text=_('Reference to site at which sampling took place'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Sampling event commentaries'),
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to sampling event'),
        default=empty_JSON,
        blank=True,
        null=True)
    started_on = models.DateTimeField(
        db_column='started_on',
        verbose_name=_('started on'),
        help_text=_('Date at which sampling begun'),
        blank=True,
        null=True)
    ended_on = models.DateTimeField(
        db_column='ended_on',
        verbose_name=_('ended on'),
        help_text=_('Date at which sampling stoped'),
        blank=True,
        null=True)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.PROTECT,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which sampling event belongs'),
        blank=False,
        null=False)
    licence = models.ForeignKey(
        'Licence',
        on_delete=models.PROTECT,
        db_column='licence_id',
        verbose_name=_('licence'),
        help_text=_('Licence for all items in sampling event'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Sampling Event')
        verbose_name_plural = _('Sampling Events')

        ordering = ['-created_on']

    def __str__(self):
        msg = _('%(site)s - %(date)s')
        params = dict(
            site=str(self.collection_site),
            date=self.started_on.strftime('%m/%Y'))
        return msg % params

    @property
    def items(self):
        queryset = Item.objects.filter(
            sampling_event_device__sampling_event=self)
        return queryset

    def validate_site(self):
        collection = self.collection
        site_collection = self.collection_site.collection

        if collection != site_collection:
            msg = _(
                'Site does not belong to the declared collection')
            raise ValidationError(msg)

    def validate_dates(self):
        if self.started_on > self.ended_on:
            msg = _(
                'Starting date cannot be greater than ending date')
            raise ValidationError(msg)

    def validate_date(self, date_info):
        pass

    def clean(self):
        collection = self.collection

        try:
            self.validate_site()
        except ValidationError as error:
            raise ValidationError({'collection_site': str(error)})

        try:
            self.validate_dates()
        except ValidationError as error:
            raise ValidationError({'started_on': str(error)})

        try:
            self.sampling_event_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': str(error)})

        try:
            site_type = self.collection_site.site_type
            self.sampling_event_type.validate_site_type(site_type)
        except ValidationError as error:
            raise ValidationError({'collection_site': str(error)})

        try:
            collection.validate_and_get_sampling_event_type(self.sampling_event_type)
        except ValidationError as error:
            raise ValidationError({'sampling_event_type': str(error)})

        if self.licence:
            try:
                collection.validate_and_get_licence(self.licence)
            except ValidationError as error:
                raise ValidationError({'licence': str(error)})

        super(SamplingEvent, self).clean()
