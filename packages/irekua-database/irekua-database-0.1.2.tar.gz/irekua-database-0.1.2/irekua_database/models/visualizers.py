from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _

from irekua_database.models import base

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema


class Visualizer(base.IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of visualizer app'),
        blank=False,
        null=False)
    version = models.CharField(
        max_length=16,
        db_column='version',
        verbose_name=_('version'),
        help_text=_('Version of visualizer app'),
        blank=False,
        null=False)
    website = models.URLField(
        db_column='website',
        verbose_name=_('website'),
        help_text=_('Link to visualizer website'),
        blank=True)
    configuration_schema = JSONField(
        db_column='configuration_schema',
        verbose_name=_('configuration schema'),
        help_text=_('JSON schema for annotation tool configuration info'),
        blank=True,
        null=False,
        validators=[validate_JSON_schema],
        default=simple_JSON_schema)

    class Meta:
        verbose_name = _('Visualizer')
        verbose_name_plural = _('Visualizers')

        ordering = ['-created_on']
        unique_together = (
            ('name', 'version'),
        )

    def validate_configuration(self, configuration):
        try:
            validate_JSON_instance(
                schema=self.configuration_schema,
                instance=configuration)
        except ValidationError as error:
            msg = _('Invalid visualizer configuration. Error: %(error)s')
            params = dict(error=str(error))
            raise ValidationError(msg, params=params)

    def __str__(self):
        return '{}@{}'.format(self.name, self.version)
