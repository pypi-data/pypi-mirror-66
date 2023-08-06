from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class Synonym(base.IrekuaModelBase):
    source = models.ForeignKey(
        'Term',
        related_name='synonym_source',
        on_delete=models.CASCADE,
        db_column='source_id',
        verbose_name=_('source'),
        help_text=_('Reference to the source of synonym'),
        blank=False)
    target = models.ForeignKey(
        'Term',
        related_name='synonym_target',
        on_delete=models.CASCADE,
        db_column='target_id',
        verbose_name=_('target'),
        help_text=_('Reference to the target of the synonym'),
        blank=False)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        default=empty_JSON,
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to the synonym'),
        null=True)

    class Meta:
        verbose_name = _('Synonym')
        verbose_name_plural = _('Synonyms')

        ordering = ['source']

    def __str__(self):
        msg = '%(source)s = %(target)s'
        params = dict(
            source=str(self.source),
            target=str(self.target))
        return msg % params

    def clean(self):
        if self.source.term_type != self.target.term_type:
            msg = _('Source and target terms are not of the same type')
            raise ValidationError({'target': msg})

        try:
            self.source.term_type.validate_synonym_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        super(Synonym, self).clean()
