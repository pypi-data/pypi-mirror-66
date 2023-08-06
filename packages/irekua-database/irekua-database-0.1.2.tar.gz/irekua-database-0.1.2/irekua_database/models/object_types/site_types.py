from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import JSONField

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema

from irekua_database.models import base


class SiteType(base.IrekuaModelBase):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of site type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of site type'),
        blank=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of site info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    site_descriptor_types = models.ManyToManyField(
        'SiteDescriptorType',
        blank=True)

    class Meta:
        verbose_name = _('Site Type')
        verbose_name_plural = _('Site Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_descriptor_type(self, descriptor):
        try:
            self.site_descriptor_types.get(pk=descriptor.descriptor_type.pk)
        except self.site_descriptor_types.model.DoesNotExist:
            msg = _(
                'This site type does not accept descriptors of type %(descriptor_type)s')
            params = dict(descriptor_type=descriptor.descriptor_type)
            raise ValidationError(msg, params=params)

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _('Invalid site metadata for site of type %(type)s. Error: %(error)')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)
