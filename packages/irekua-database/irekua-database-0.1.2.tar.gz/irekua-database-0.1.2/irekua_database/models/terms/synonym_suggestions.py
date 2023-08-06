from django.contrib.postgres.fields import JSONField
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class SynonymSuggestion(base.IrekuaModelBaseUser):
    source = models.ForeignKey(
        'Term',
        on_delete=models.CASCADE,
        db_column='source_id',
        verbose_name='')
    synonym = models.CharField(
        max_length=128,
        db_column='synonym',
        verbose_name=_('synonym'),
        help_text=_('Suggestion of synonym'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of synonym'),
        blank=True)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to synonym'),
        default=empty_JSON,
        null=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = _('Synonym Suggestion')
        verbose_name = _('Synonym Suggestions')

    def __str__(self):
        msg = _('Suggestion: {term} = {suggestion}').format(
            term=str(self.source),
            suggestion=self.synonym)
        return msg

    def clean(self):
        try:
            self.source.term_type.validate_synonym_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        super(SynonymSuggestion, self).clean()
