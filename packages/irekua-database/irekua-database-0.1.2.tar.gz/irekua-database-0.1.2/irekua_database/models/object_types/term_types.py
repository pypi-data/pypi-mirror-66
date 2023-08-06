from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema

from irekua_database.models import base


class TermType(base.IrekuaModelBase):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for term type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of term type'),
        blank=False)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Term type icon'),
        upload_to='images/term_types/',
        blank=True,
        null=True)
    is_categorical = models.BooleanField(
        db_column='is_categorical',
        verbose_name=_('is categorical'),
        help_text=_(
            'Flag indicating whether the term type represents '
            'a categorical variable'),
        blank=False,
        null=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of term info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])
    synonym_metadata_schema = JSONField(
        db_column='synonym_metadata_schema',
        verbose_name=_('synonym metadata schema'),
        help_text=_('JSON Schema for metadata of synonym info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Term Type')
        verbose_name_plural = _('Term Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_non_categorical_value(self, value):
        if not isinstance(value, (int, float)):
            msg = _(
                'Value %(value)s is invalid for non-categorical '
                'term of type %(type)s')
            params = dict(value=value, type=str(self))
            raise ValidationError(msg % params)

    def validate_categorical_value(self, value):
        if not self.term_set.filter(value=value).exists():
            msg = _(
                'Value %(value)s is invalid for categorical term '
                'of type %(type)s')
            params = dict(value=value, type=str(self))
            raise ValidationError(msg % params)

    def validate_value(self, value):
        if self.is_categorical:
            return self.validate_categorical_value(value)

        return self.validate_non_categorical_value(value)

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _(
                'Invalid metadata for term of type %(type)s. '
                'Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg % params)

    def validate_synonym_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.synonym_metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _(
                'Invalid metadata for synonym of terms of type '
                '%(type)s. Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg % params)
