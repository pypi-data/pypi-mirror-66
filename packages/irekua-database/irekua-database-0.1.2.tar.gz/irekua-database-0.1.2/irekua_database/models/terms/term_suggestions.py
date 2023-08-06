from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class TermSuggestion(base.IrekuaModelBaseUser):
    term_type = models.ForeignKey(
        'TermType',
        on_delete=models.CASCADE,
        db_column='term_type',
        verbose_name=_('term type'),
        help_text=_('Type of term'),
        blank=False,
        null=False)
    value = models.CharField(
        max_length=128,
        db_column='value',
        verbose_name=_('value'),
        help_text=_('Value of term'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of term'),
        blank=True)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        default=empty_JSON,
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to term'),
        null=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = _('Term Suggestion')
        verbose_name = _('Term Suggestions')

    def __str__(self):
        msg = _('Suggestion: %(term_type)s: %(value)s')
        params = dict(
            term_type=str(self.term_type),
            value=self.value)
        return msg % params

    def clean(self, *args, **kwargs):
        try:
            self.term_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        super(TermSuggestion, self).clean(*args, **kwargs)
