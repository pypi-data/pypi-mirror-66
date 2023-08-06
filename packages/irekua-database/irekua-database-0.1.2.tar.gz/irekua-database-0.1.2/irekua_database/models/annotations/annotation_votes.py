from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class AnnotationVote(base.IrekuaModelBaseUser):
    annotation = models.ForeignKey(
        'Annotation',
        on_delete=models.CASCADE,
        db_column='annotation_id',
        verbose_name=_('annotation'),
        help_text=_('Reference to annotation being voted'),
        blank=False,
        null=False)
    labels = models.ManyToManyField(
        'Term',
        db_column='labels',
        verbose_name=_('labels'),
        help_text=_('Labels associated with annotation'),
        blank=True)

    class Meta:
        ordering = ['-modified_on']
        verbose_name = _('Annotation Vote')
        verbose_name_plural = _('Annotation Votes')

    def __str__(self):
        msg = _('Vote %(id)s on annotation %(annotation)s')
        params = dict(id=self.id, annotation=self.annotation.id)
        return msg % params

    def clean(self):
        if self.id:
            try:
                self.validate_labels(self.labels.all())
            except ValidationError as error:
                raise ValidationError({'labels': error})

        super().clean()

    def validate_labels(self, labels):
        for term in labels:
            term_type = term.term_type.name
            try:
                self.annotation.event_type.validate_term_type(term_type)
            except ValidationError:
                msg = _(
                        'Labels contain a term (of type %(type)s) that is not '
                        'valid for the event type')
                params = dict(type=term_type)
                raise ValidationError(msg, params=params)
