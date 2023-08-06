import mimetypes
import os

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.utils import hash_file
from irekua_database.models import base


mimetypes.init()


def get_item_path(instance, filename):
    path_fmt = os.path.join(
        'secondary_items',
        '{collection}',
        '{sampling_event}',
        '{sampling_event_device}',
        '{hash}',
        '{secondary_hash}{ext}')

    extension = mimetypes.guess_extension(
        instance.item_type.media_type)
    item = instance.item
    sampling_event_device = item.sampling_event_device
    sampling_event = sampling_event_device.sampling_event
    collection = sampling_event.collection

    instance.item_file.open()
    hash_string = hash_file(instance.item_file)

    path = path_fmt.format(
        collection=collection.pk,
        sampling_event=sampling_event.pk,
        sampling_event_device=sampling_event_device.pk,
        hash=item.hash,
        secondary_hash=hash_string,
        ext=extension)
    return path


class SecondaryItem(base.IrekuaModelBase):
    hash = models.CharField(
        max_length=64,
        unique=True,
        db_column='hash',
        verbose_name=_('hash'),
        help_text=_('Hash of secondary resource file'),
        blank=False)
    item_file = models.FileField(
        upload_to=get_item_path,
        db_column='item_file',
        verbose_name=_('item file'),
        help_text=_('Upload file associated to file'),
        blank=True,
        null=True)
    item_type = models.ForeignKey(
        'ItemType',
        on_delete=models.PROTECT,
        db_column='item_type',
        verbose_name=_('item type'),
        help_text=_('Type of file of secondary item'),
        blank=False,
        null=False)
    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item id'),
        help_text=_('Reference to primary item associated to secondary item'),
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    media_info = JSONField(
        db_column='media_info',
        verbose_name=_('media info'),
        help_text=_('Media information of secondary item file'),
        default=empty_JSON,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Secondary Item')
        verbose_name_plural = _('Secondary Items')

        ordering = ['created_on']

    def __str__(self):
        msg = _('Secondary Item %(id)s derived from %(itemid)s')
        params = dict(
            id=self.id,  # pylint: disable=E1101
            itemid=str(self.item))
        return msg % params

    def validate_hash(self):
        if self.item_file.name is None and self.hash is None:
            msg = _(
                'If no file is provided, a hash must be given')
            raise ValidationError(msg)

        if self.item_file.name is None:
            return

        self.item_file.open()  # pylint: disable=E1101
        hash_string = hash_file(self.item_file)

        if self.hash is None:
            self.hash = hash_string

        if self.hash != hash_string:
            msg = _('Hash of file and recorded hash do not coincide')
            raise ValidationError(msg)

    def clean(self):
        try:
            self.item_type.validate_media_info(self.media_info)  # pylint: disable=E1101
        except ValidationError as error:
            raise ValidationError({'media_info': error})

        try:
            self.validate_hash()
        except ValidationError as error:
            raise ValidationError({'hash': error})

        super(SecondaryItem, self).clean()
