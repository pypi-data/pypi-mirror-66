import mimetypes
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema

from irekua_database.models import base


mimetypes.init()


class MimeType(base.IrekuaModelBase):
    MIME_TYPES = [
        (value, value) for value in
        sorted(list(set(mimetypes.types_map.values())))
    ]

    mime_type = models.CharField(
        max_length=128,
        unique=True,
        choices=MIME_TYPES,
        db_column='media_type',
        verbose_name=_('media type'),
        help_text=_('MIME types associated with item type'),
        blank=False)
    media_info_schema = JSONField(
        db_column='media_info_schema',
        verbose_name=_('media info schema'),
        help_text=_('JSON Schema for item type media info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Mime Type')
        verbose_name_plural = _('Mime Types')

        ordering = ['mime_type']

    def __str__(self):
        return self.mime_type

    def validate_media_info(self, media_info):
        try:
            validate_JSON_instance(
                schema=self.media_info_schema,
                instance=media_info)
        except ValidationError as error:
            msg = _(
                'Invalid media info for item of type %(type)s. '
                'Error %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)
