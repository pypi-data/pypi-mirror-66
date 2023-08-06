import mimetypes
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.models import base


mimetypes.init()


class ItemType(base.IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        unique=True,
        help_text=_('Name of item type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of item type'),
        blank=False)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Item type icon'),
        upload_to='images/item_types/',
        blank=True,
        null=True)

    mime_types = models.ManyToManyField(
        'MimeType',
        db_column='mime_types',
        verbose_name=_('mime types'),
        help_text=_('Mime types of files for this item type'),
        blank=True)
    event_types = models.ManyToManyField(
        'EventType',
        db_column='event_types',
        verbose_name=_('event types'),
        help_text=_('Types of event for this item type'),
        blank=True)

    class Meta:
        verbose_name = _('Item Type')
        verbose_name_plural = _('Item Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_item_type(self, item):
        mime_type_from_file, encoding = mimetypes.guess_type(item.item_file.url)

        try:
            mime_type = self.mime_types.get(mime_type=mime_type_from_file)
        except self.mime_types.model.DoesNotExist:
            msg = _(
                'This item type does not accept files of type %(mime_type)s')
            params = dict(mime_type=mime_type_from_file)
            raise ValidationError(msg, params=params)

        mime_type.validate_media_info(item.media_info)

    def validate_and_get_event_type(self, event_type):
        try:
            return self.event_types.get(name=event_type.name)
        except self.event_types.model.DoesNotExist:
            msg = _(
                'Event type %(event_type)s is invalid for item '
                'type %(item_type)s')
            params = dict(event_type=str(event_type), item_type=str(self))
            raise ValidationError(msg, params=params)

    def add_event_type(self, event_type):
        self.event_types.add(event_type)

    def remove_event_type(self, event_type):
        self.event_types.remove(event_type)

    def add_event_type(self, mime_type):
        self.mime_types.add(mime_type)

    def remove_event_type(self, mime_type):
        self.mime_types.remove(mime_type)
