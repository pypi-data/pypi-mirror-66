from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema


class LocalityType(models.Model):
    name = models.CharField(
        max_length=128,
        db_column='name',
        unique=True,
        help_text=_('Name of locality'))
    description = models.TextField(
        blank=True,
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of type of locality'))
    source = models.URLField(
        max_length=128,
        blank=True,
        db_column='source',
        verbose_name=_('source'),
        help_text=_('Source of information for localities of this type'))
    original_datum = models.TextField(
        blank=True,
        db_column='original_datum',
        verbose_name=_('original datum'),
        help_text=_(
            'Datum used for the original coordinates for localities'
            ' of this type in WTK format'))
    publication_date = models.DateField(
        blank=True,
        db_column='publication_date',
        verbose_name=_('publication date'),
        help_text=_('Date of publication of localities defined in this type'))

    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata_schema'),
        help_text=_('JSON Schema for metadata of localities of this type'),
        default=simple_JSON_schema,
        validators=[validate_JSON_schema],
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Locality Type')
        verbose_name_plural = _('Locality Types')

        ordering = ['-name']

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _('Invalid locality metadata. Error: %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)

    def __str__(self):
        return self.name
