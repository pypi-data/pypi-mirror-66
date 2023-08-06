from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import JSONField

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema

from irekua_database.models import base


class LicenceType(base.IrekuaModelBase):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Licence type name'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of licence'),
        blank=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of licence info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])
    document_template = models.FileField(
        upload_to='documents/licence_types/',
        db_column='document_template',
        verbose_name=_('document template'),
        help_text=_('Template for licence document'),
        blank=True,
        null=True)
    years_valid_for = models.IntegerField(
        db_column='years_valid_for',
        verbose_name=_('years valid for'),
        help_text=_(
            'Number of years for which licences of this type '
            'are valid'),
        blank=False,
        null=False)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Licence type icon'),
        upload_to='images/licence_types/',
        blank=True,
        null=True)

    can_view = models.BooleanField(
        db_column='can_view',
        verbose_name=_('can view'),
        help_text=_('Any user can view item info'),
        blank=False,
        null=False)
    can_download = models.BooleanField(
        db_column='can_download',
        verbose_name=_('can download'),
        help_text=_('Any user can download item'),
        blank=False,
        null=False)
    can_view_annotations = models.BooleanField(
        db_column='can_view_annotations',
        verbose_name=_('can view annotations'),
        help_text=_('Any user can view item annotations'),
        blank=False,
        null=False)
    can_annotate = models.BooleanField(
        db_column='can_annotate',
        verbose_name=_('can annotate'),
        help_text=_('Any user can annotate item'),
        blank=False,
        null=False)
    can_vote_annotations = models.BooleanField(
        db_column='can_vote_annotations',
        verbose_name=_('can vote annotations'),
        help_text=_('Any user can vote on item annotations'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Licence Type')
        verbose_name_plural = _('Licence Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _('Invalid licence metadata. Error: %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)
