from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class SiteDescriptor(base.IrekuaModelBase):
    descriptor_type = models.ForeignKey(
        'SiteDescriptorType',
        on_delete=models.CASCADE,
        db_column='descriptor_type',
        verbose_name=_('descriptor type'),
        help_text=_('Type of site descriptor'),
        blank=False,
        null=False)
    value = models.CharField(
        max_length=128,
        db_column='value',
        verbose_name=_('value'),
        help_text=_('Value of descriptor'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of term'),
        blank=True)

    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to term'),
        default=empty_JSON,
        blank=True,
        null=True)

    class Meta:
        ordering = ['descriptor_type', 'value']
        verbose_name = _('Site Descriptor')
        verbose_name_plural = _('Site Descriptors')
        unique_together = (('descriptor_type', 'value'))

    def __str__(self):
        msg = '{descriptor_type}: {value}'.format(
            descriptor_type=self.descriptor_type,
            value=self.value)
        return msg

    def clean(self, *args, **kwargs):
        try:
            self.descriptor_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        super().clean(*args, **kwargs)
