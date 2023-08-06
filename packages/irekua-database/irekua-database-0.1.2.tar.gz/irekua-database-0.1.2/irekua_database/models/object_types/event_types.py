from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.models import base


class EventType(base.IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of event type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of event type'),
        blank=False)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Event type icon'),
        upload_to='images/event_types/',
        blank=True,
        null=True)

    term_types = models.ManyToManyField(
        'TermType',
        db_column='term_types',
        verbose_name=_('term types'),
        help_text=_(
            'Valid term types with which to label this type '
            'of events'),
        blank=True)
    should_imply = models.ManyToManyField(
        'Term',
        db_column='should_imply',
        verbose_name='should imply',
        help_text=_(
            'Terms that should be implied (if meaningful) by '
            'any terms used to describe this event type.'),
        blank=True)

    class Meta:
        verbose_name = _('Event Type')
        verbose_name_plural = _('Event Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_term_type(self, term_type):
        try:
            self.term_types.get(name=term_type)
        except self.term_types.model.DoesNotExist:
            msg = _(
                'Term type %(term_type)s is invalid for event '
                'type %(event_type)s')
            params = dict(term_type=str(term_type), event_type=str(self))
            raise ValidationError(msg, params=params)

    def add_term_type(self, term_type):
        self.term_types.add(term_type)

    def remove_term_type(self, term_type):
        self.term_types.remove(term_type)
