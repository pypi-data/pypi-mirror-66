from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.models import base


class AnnotationTool(base.IrekuaModelBase):
    annotation_type = models.ForeignKey(
        'AnnotationType',
        on_delete=models.CASCADE,
        db_column='annotation_type_id',
        verbose_name=_('annotation type'),
        help_text=_('Type of annotation this tool produces'))
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of annotation tool'),
        blank=False)
    version = models.CharField(
        max_length=16,
        db_column='version',
        verbose_name=_('version'),
        help_text=_('Version of annotation tool'),
        blank=False)
    logo = models.ImageField(
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Annotation tool logo'),
        upload_to='images/annotation_tools/',
        blank=True,
        null=True)
    website = models.URLField(
        db_column='website',
        verbose_name=_('website'),
        help_text=_('Annotation tool website'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Annotation Tool')
        verbose_name_plural = _('Annotation Tools')

        unique_together = (('name', 'version'))

        ordering = ['name']

    def __str__(self):
        return '{}@{}'.format(self.name, self.version)
