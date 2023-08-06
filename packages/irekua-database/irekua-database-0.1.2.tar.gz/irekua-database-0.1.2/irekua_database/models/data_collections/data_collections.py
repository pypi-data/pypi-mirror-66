from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.utils import empty_JSON
from irekua_database.models import base
from irekua_database.models.items.items import Item
from irekua_database.models.annotations.annotations import Annotation

from .collection_users import CollectionUser
from .collection_devices import CollectionDevice
from .collection_sites import CollectionSite


class Collection(base.IrekuaModelBaseUser):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.PROTECT,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Type of collection'),
        blank=False,
        null=False)
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of collection'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of collection'),
        blank=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to collection'),
        blank=True,
        default=empty_JSON,
        null=False)
    institution = models.ForeignKey(
        'Institution',
        on_delete=models.PROTECT,
        db_column='institution_id',
        verbose_name=_('institution'),
        help_text=_('Institution to which the collection belogs'),
        blank=True,
        null=True)
    logo = models.ImageField(
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Logo of data collection'),
        upload_to='images/collections/',
        blank=True,
        null=True)

    physical_devices = models.ManyToManyField(
        'PhysicalDevice',
        through='CollectionDevice',
        through_fields=('collection', 'physical_device'),
        blank=True)
    sites = models.ManyToManyField(
        'Site',
        through='CollectionSite',
        through_fields=('collection', 'site'),
        blank=True)
    users = models.ManyToManyField(
        'User',
        related_name='collection_users',
        through='CollectionUser',
        through_fields=('collection', 'user'),
        blank=True)
    administrators = models.ManyToManyField(
        'User',
        related_name='collection_administrators',
        verbose_name=_('administrators'),
        help_text=_('Administrators of collection'),
        blank=True)

    is_open = models.BooleanField(
        db_column='is_open',
        verbose_name=_('is open'),
        help_text=_(
            'Boolean flag indicating whether contents of the collection are public.'),
        blank=True,
        null=False,
        default=False)

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')

        permissions = (
            (
                "add_collection_site",
                _("Can add site to collection")),
            (
                "add_collection_item",
                _("Can add item to collection")),
            (
                "add_collection_device",
                _("Can add device to collection")),
            (
                "add_collection_sampling_event",
                _("Can add a sampling event to collection")),
            (
                "add_collection_user",
                _("Can add user to collection")),
            (
                "add_collection_licence",
                _("Can add licence to collection")),
            (
                "add_collection_annotation",
                _("Can annotate items in collection")),
            (
                "add_collection_annotation_vote",
                _("Can vote on annotations of items in collection")),
            (
                "view_collection_sites",
                _("Can view sites in collection")),
            (
                "view_collection_items",
                _("Can view items in collection")),
            (
                "view_collection_devices",
                _("Can view devices in collection")),
            (
                "view_collection_sampling_events",
                _("Can view sampling event in collection")),
            (
                "view_collection_annotations",
                _("Can view annotations of items in collection")),
            (
                "change_collection_sites",
                _("Can change sites in collection")),
            (
                "change_collection_users",
                _("Can change user info in collection")),
            (
                "change_collection_items",
                _("Can change items in collection")),
            (
                "change_collection_devices",
                _("Can change devices in collection")),
            (
                "change_collection_annotations",
                _("Can change annotations of items in collection")),
            (
                "change_collection_sampling_events",
                _("Can change sampling events in collection")),
            (
                "download_collection_items",
                _("Can download annotation items")),
        )

        ordering = ['-created_on']

    def __str__(self):
        return self.name

    def clean(self):
        try:
            self.collection_type.validate_metadata(self.metadata)  # pylint: disable=E1101
        except ValidationError as error:
            msg = _(
                'Invalid metadata for collection of type {type}. '
                'Error: {error}')
            msg = msg.format(  # pylint: disable=E1101
                type=str(self.collection_type),
                error=str(error))
            raise ValidationError({'metadata': msg})
        super(Collection, self).clean()

    def add_administrator(self, user):
        self.administrators.add(user)
        self.save()

    def remove_administrator(self, user):
        self.administrators.remove(user)
        self.save()

    @property
    def all_admin(self):
        return self.administrators.all()

    @property
    def items(self):
        return Item.objects.filter(
            sampling_event_device__sampling_event__collection=self)

    @property
    def last_item(self):
        return Item.objects.filter(
            sampling_event_device__sampling_event__collection=self
        ).order_by('created_on').first()

    @property
    def annotations(self):
        return Annotation.objects.filter(
            item__sampling_event_device__sampling_event__collection=self
        )

    @property
    def last_annotation(self):
        return Annotation.objects.filter(
            item__sampling_event_device__sampling_event__collection=self
        ).order_by('created_on').first()

    def add_user(self, user, role, metadata):
        CollectionUser.objects.create(  # pylint: disable=E1101
            collection=self,
            user=user,
            role=role,
            metadata=metadata)

    def add_site(self, site, internal_id, site_type=None, metadata=None):
        if metadata is None:
            metadata = {}

        CollectionSite.objects.create(  # pylint: disable=E1101
            collection=self,
            site=site,
            internal_id=internal_id,
            site_type=site_type,
            metadata=metadata)

    def add_device(self, physical_device, internal_id, metadata):
        CollectionDevice.objects.create(  # pylint: disable=E1101
            collection=self,
            physical_device=physical_device,
            internal_id=internal_id,
            metadata=metadata)

    def validate_and_get_annotation_type(self, annotation_type):
        return self.collection_type.validate_and_get_annotation_type(  # pylint: disable=E1101
            annotation_type)

    def validate_and_get_event_type(self, event_type):
        return self.collection_type.validate_and_get_event_type(event_type)  # pylint: disable=E1101

    def validate_and_get_site_type(self, site_type):
        return self.collection_type.validate_and_get_site_type(site_type)  # pylint: disable=E1101

    def validate_and_get_device_type(self, device_type):
        return self.collection_type.validate_and_get_device_type(device_type)  # pylint: disable=E1101

    def validate_and_get_item_type(self, item_type):
        return self.collection_type.validate_and_get_item_type(item_type)  # pylint: disable=E1101

    def validate_and_get_sampling_event_type(self, sampling_event_type):
        return self.collection_type.validate_and_get_sampling_event_type(  # pylint: disable=E1101
            sampling_event_type)

    def validate_and_get_licence_type(self, licence_type):
        return self.collection_type.validate_and_get_licence_type(licence_type)  # pylint: disable=E1101

    def validate_and_get_role(self, role):
        return self.collection_type.validate_and_get_role(role)  # pylint: disable=E1101

    def validate_and_get_licence(self, licence):
        try:
            licence = self.licence_set.get(pk=licence.pk)  # pylint: disable=E1101
        except self.licences.model.DoesNotExist:  # pylint: disable=E1101
            msg = _(
                'Licence %(licence)s is not part of collection '
                '%(collection)s.')
            params = dict(
                licence=str(licence),
                collection=str(self))
            raise ValidationError(msg, params=params)

    def is_admin(self, user):
        queryset = self.administrators.filter(id=user.id)  # pylint: disable=E1101
        return queryset.exists()

    def is_user(self, user):
        try:
            self.users.get(pk=user.pk)
            return True
        except self.users.model.DoesNotExist:
            return False

    def has_user(self, user):
        return CollectionUser.objects.filter(  # pylint: disable=E1101
            collection=self,
            user=user).exists()

    def has_permission(self, user, codename):
        try:
            collectionuser = CollectionUser.objects.get(  # pylint: disable=E1101
                collection=self,
                user=user)
            role = collectionuser.role
        except CollectionUser.DoesNotExist:  # pylint: disable=E1101
            return False

        return role.has_permission(codename)

    def get_user_role(self, user):
        try:
            collection_user = CollectionUser.objects.get(  # pylint: disable=E1101
                collection=self,
                user=user)
            return collection_user.role
        except CollectionUser.DoesNotExist:
            return None

    def update_is_open(self):
        restrictive_licences = self.licence_set.filter(
            is_active=True,
            licence_type__can_view=False)

        self.is_open = not restrictive_licences.exits()
        self.save()
