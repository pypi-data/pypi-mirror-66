from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base


class Annotation(base.IrekuaModelBaseUser):
    LOW = 'L'
    MEDIUM = 'M'
    HIGH = 'H'
    CERTAINTY_OPTIONS = [
        (LOW, _('uncertain')),
        (MEDIUM, _('somewhat certain')),
        (HIGH, _('certain')),
    ]
    QUALITY_OPTIONS = [
        (LOW, _('low')),
        (MEDIUM, _('medium')),
        (HIGH, _('high')),
    ]

    annotation_tool = models.ForeignKey(
        'AnnotationTool',
        on_delete=models.PROTECT,
        db_column='annotation_tool_id',
        verbose_name=_('annotation tool'),
        help_text=_('Annotation tool used when annotating'),
        blank=False)
    visualizer = models.ForeignKey(
        'Visualizer',
        on_delete=models.PROTECT,
        db_column='visualizers_id',
        verbose_name=_('visualizer'),
        help_text=_('Visualizer used when annotating'),
        blank=False)
    item = models.ForeignKey(
        'Item',
        db_column='item_id',
        verbose_name=_('item'),
        help_text=_('Annotated item'),
        on_delete=models.PROTECT,
        blank=False)
    event_type = models.ForeignKey(
        'EventType',
        on_delete=models.PROTECT,
        db_column='event_type_id',
        verbose_name=_('event type'),
        help_text=_('Type of event being annotated'),
        blank=False)
    annotation_type = models.ForeignKey(
        'AnnotationType',
        on_delete=models.PROTECT,
        db_column='annotation_type_id',
        verbose_name=_('annotation type'),
        help_text=_('Type of annotation'),
        blank=False)
    annotation = JSONField(
        db_column='annotation',
        verbose_name=_('annotation'),
        default=empty_JSON,
        help_text=_('Information of annotation location within item'),
        blank=True,
        null=False)
    visualizer_configuration = JSONField(
        db_column='visualizer_configuration',
        verbose_name=_('visualizer configuration'),
        default=empty_JSON,
        help_text=_('Configuration of visualizer at annotation creation'),
        blank=True,
        null=False)
    certainty = models.CharField(
        max_length=16,
        db_column='certainty',
        verbose_name=_('certainty'),
        help_text=_(
            'Level of certainty of location or labelling '
            'of annotation'),
        blank=True,
        choices=CERTAINTY_OPTIONS,
        null=True)
    quality = models.CharField(
        db_column='quality',
        verbose_name=_('quality'),
        help_text=_('Quality of item content inside annotation'),
        blank=True,
        max_length=16,
        choices=QUALITY_OPTIONS)
    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Commentaries of annotator'),
        blank=True)

    labels = models.ManyToManyField(
        'Term',
        db_column='labels',
        verbose_name=_('labels'),
        help_text=_('Labels associated with annotation'),
        blank=True)

    class Meta:
        verbose_name = _('Annotation')
        verbose_name_plural = _('Annotations')

        ordering = ['-modified_on']

        permissions = (
            ("vote", _("Can vote annotation")),
        )

    def __str__(self):
        msg = _('Annotation of item %(item_id)s')
        params = dict(item_id=self.item)
        return msg % params

    def clean(self):
        try:
            self.item.validate_and_get_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error})

        collection = self.item.sampling_event_device.sampling_event.collection
        try:
            collection.validate_and_get_event_type(self.event_type)
        except ValidationError as error:
            raise ValidationError({'event_type': error})

        try:
            collection.validate_and_get_annotation_type(self.annotation_type)
        except ValidationError as error:
            raise ValidationError({'annotation_type': error})

        try:
            self.annotation_type.validate_annotation(self.annotation)
        except ValidationError as error:
            raise ValidationError({'annotation': error})

        if self.annotation_type != self.annotation_tool.annotation_type:
            msg = _('Invalid annotation tool for this annotation type')
            raise ValidationError({'annotation_tool': msg})

        try:
            self.visualizer.validate_configuration(
                self.visualizer_configuration)
        except ValidationError as error:
            raise ValidationError({'visualizer_configuration': error})

        if self.id:
            try:
                self.validate_labels(self.labels.all())
            except ValidationError as error:
                raise ValidationError({'labels': error})

        super(Annotation, self).clean()

    def validate_labels(self, labels):
        for term in labels:
            term_type = term.term_type.name
            try:
                self.event_type.validate_term_type(term_type)
            except ValidationError:
                msg = _(
                    'Labels contain a term (of type %(type)s) that is not '
                    'valid for the event type')
                params = dict(type=term_type)
                raise ValidationError(msg, params=params)
