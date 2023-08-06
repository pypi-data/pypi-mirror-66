from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models import base


class Source(base.IrekuaModelBase):
    directory = models.CharField(
        max_length=64,
        unique=True,
        db_column='directory',
        verbose_name=_('directory'),
        help_text=_('Directory containing all files in source'),
        blank=False)
    source_file = models.CharField(
        max_length=64,
        db_column='source_file',
        verbose_name=_('source file'),
        help_text=_('File containing metadata for files in source directory'),
        blank=False)
    parse_function = models.CharField(
        max_length=64,
        db_column='parse_function',
        verbose_name=_('parse function'),
        help_text=_('Parse function used to insert files and metadata to database'),
        blank=False)
    uploader = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        db_column='uploader_id',
        verbose_name=_('uploader id'),
        help_text=_('Reference to user who uploaded files in source'),
        related_name='source_uploader',
        blank=False)

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

    def __str__(self):
        msg = _('Directory %(dir)s uploaded with %(func)s')
        params = dict(
            dir=self.directory,
            func=self.parse_function)
        return msg % params
