from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class Term(base.IrekuaModelBase):
    term_type = models.ForeignKey(
        'TermType',
        on_delete=models.CASCADE,
        db_column='term_type',
        verbose_name=_('term type'),
        help_text=_('Type of term'),
        limit_choices_to={'is_categorical': True},
        blank=False,
        null=False)
    value = models.CharField(
        max_length=128,
        db_column='value',
        verbose_name=_('value'),
        help_text=_('Value of term'),
        blank=False)
    scope = models.CharField(
        max_length=128,
        db_column='scope',
        verbose_name=_('scope'),
        help_text=_('Scope of term. Use for disambiguation.'),
        blank=True)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of term'),
        blank=True)
    url = models.URLField(
        db_column='url',
        verbose_name=_('term url'),
        help_text=_('URL for term description'),
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to term'),
        default=empty_JSON,
        blank=True,
        null=True)

    class Meta:
        ordering = ['term_type', 'value']
        verbose_name = _('Term')
        verbose_name_plural = _('Terms')
        unique_together = (('term_type', 'value', 'scope'))

    def __str__(self):
        msg = '{term_type}: {value}'.format(
            term_type=self.term_type,
            value=self.value)
        return msg

    def clean(self, *args, **kwargs):
        try:
            self.term_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        super(Term, self).clean(*args, **kwargs)
