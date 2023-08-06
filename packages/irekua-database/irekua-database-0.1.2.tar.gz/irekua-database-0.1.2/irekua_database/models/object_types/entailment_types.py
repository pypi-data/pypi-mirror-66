from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import JSONField

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema

from irekua_database.models import base


class EntailmentType(base.IrekuaModelBase):
    source_type = models.ForeignKey(
        'TermType',
        related_name='entailment_source_type',
        db_column='source_type_id',
        verbose_name=_('source type'),
        help_text=_('Term type of source of entailment'),
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    target_type = models.ForeignKey(
        'TermType',
        related_name='entailment_target_type',
        db_column='target_type_id',
        verbose_name=_('target type'),
        help_text=_('Term type of target of entailment'),
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of entailment info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Entailment Type')
        verbose_name_plural = _('Entailment Types')
        unique_together = (('source_type', 'target_type'))

        ordering = ['source_type']

    def __str__(self):
        msg = '%(source_type)s => %(target_type)s'
        params = dict(
            source_type=str(self.source_type),
            target_type=str(self.target_type))
        return msg % params

    def clean(self):
        if self.source_type == self.target_type:
            msg = _('Entailments are not possible between terms of the same type')
            raise ValidationError({'target': msg})

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for entailment between terms of types %(entailment)s. Error: %(error)s')
            params = dict(
                entailment=str(self),
                error=str(error))
            raise ValidationError(msg, params=params)
