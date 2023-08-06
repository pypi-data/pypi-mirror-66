from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import base


class AnnotationType(base.IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for type of annotation'))
    description = models.TextField(
        null=False,
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of annotation type'))
    annotation_schema = JSONField(
        db_column='annotation_schema',
        verbose_name=_('annotation schema'),
        help_text=_('JSON Schema for annotation info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])
    icon = models.ImageField(
        db_column='icon',
        upload_to='images/annotation_types/',
        verbose_name=_('icon'),
        help_text=_('Annotation type icon'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Annotation Type')
        verbose_name_plural = _('Annotation Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_annotation(self, annotation):
        try:
            validate_JSON_instance(
                schema=self.annotation_schema,
                instance=annotation)
        except ValidationError as error:
            msg = _('Invalid annotation for annotation type %(type)s. Error: %(error)s')
            params = dict(type=str(self), error=', '.join(error.messages))
            raise ValidationError(msg, params=params)
