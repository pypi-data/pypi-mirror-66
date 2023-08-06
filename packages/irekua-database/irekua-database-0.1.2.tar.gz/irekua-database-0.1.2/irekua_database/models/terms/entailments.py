from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.models.object_types.entailment_types import EntailmentType
from irekua_database.models import base


class Entailment(base.IrekuaModelBase):
    source = models.ForeignKey(
        'Term',
        related_name='entailment_source',
        db_column='source_id',
        verbose_name=_('source'),
        help_text=_('Source of entailment'),
        on_delete=models.CASCADE,
        blank=False)
    target = models.ForeignKey(
        'Term',
        related_name='entailment_target',
        db_column='target_id',
        verbose_name=_('target'),
        help_text=_('Target of entailment'),
        on_delete=models.CASCADE,
        blank=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to entailment'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Entailment')
        verbose_name_plural = _('Entailments')

        ordering = ['source']

    def __str__(self):
        msg = '%(source)s => %(target)s'
        params = dict(
            source=str(self.source),
            target=str(self.target))
        return msg % params

    def clean(self):
        try:
            entailment_type = EntailmentType.objects.get(
                source_type=self.source.term_type,
                target_type=self.target.term_type)
        except EntailmentType.DoesNotExist:
            msg = _('Entailment between types %(source_type)s and %(target_type)s is not possible')
            params = dict(
                source_type=self.source.term_type,
                target_type=self.target.term_type)
            raise ValidationError({'target': msg % params})

        try:
            entailment_type.validate_metadata(self.metadata)
        except ValidationError as error:
            msg = _('Invalid entailment metadata. Error %(error)s')
            params = dict(error=str(error))
            raise ValidationError({'metadata': msg % params})

        super(Entailment, self).clean()
