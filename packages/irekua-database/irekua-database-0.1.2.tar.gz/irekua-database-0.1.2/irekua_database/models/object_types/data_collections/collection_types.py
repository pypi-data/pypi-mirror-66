from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import base

from .collection_device_types import CollectionDeviceType
from .collection_roles import CollectionRole
from .collection_item_types import CollectionItemType
from irekua_database.models.data_collections.collection_users import CollectionUser
from irekua_database.models.data_collections.data_collections import Collection
from irekua_database.models.items.items import Item
from irekua_database.models.annotations.annotations import Annotation


class CollectionType(base.IrekuaModelBase):
    """
    *Collection types* function as a templates for collection creation. Its
    utility stems from the fact that the configuration of a collection can be
    a tedious process and usually some preconfigured option suffices for the
    current need. Hence a collection type contains all collection behaviour
    configuration. This amounts to the following specifications:

    1. Metadata:
        Any collection created with this template must provide further metadata
        as specified by the collection type metadata schema.

    2. Creation Configuration:
        Sometimes collection types can also serve to categorize collections and
        thus creation of collections of this types must not be free. A flag
        (anyone_can_create) has been included to indicate whether any user can
        create a collection of this type. If creation is restricted, then
        administrators must be specified. Administrators will have all permissions
        on children collections, and they alone have the permissions to create
        collections of this type.

        # TODO
    """
    name = models.CharField(
        max_length=128,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of collection type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of collection type'),
        blank=False)
    logo = models.ImageField(
        upload_to='images/collection_types/',
        db_column='logo',
        verbose_name=_('logo'),
        help_text=_('Logo of collection type'),
        blank=True,
        null=True)
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of collection info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    anyone_can_create = models.BooleanField(
        db_column='anyone_can_create',
        verbose_name=_('anyone can create'),
        help_text=_(
            'Boolean flag indicating wheter any user can '
            'create collections of this type'),
        blank=True,
        default=False,
        null=False
    )
    administrators = models.ManyToManyField(
        'User',
        verbose_name=_('administrators'),
        help_text=_(
            'Administrators of this collection type. Administrators can '
            'create collections of this type'),
        blank=True)

    restrict_site_types = models.BooleanField(
        db_column='restrict_site_types',
        verbose_name=_('restrict site types'),
        help_text=_(
            'Flag indicating whether types of sites are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)
    restrict_annotation_types = models.BooleanField(
        db_column='restrict_annotation_types',
        verbose_name=_('restrict annotation types'),
        help_text=_(
            'Flag indicating whether types of annotations are restricted '
            'to registered ones'),
        default=True,
        null=False,
        blank=True)
    restrict_item_types = models.BooleanField(
        db_column='restrict_item_types',
        verbose_name=_('restrict item types'),
        help_text=_(
            'Flag indicating whether types of items are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)
    restrict_licence_types = models.BooleanField(
        db_column='restrict_licence_types',
        verbose_name=_('restrict licence types'),
        help_text=_(
            'Flag indicating whether types of licences are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)
    restrict_device_types = models.BooleanField(
        db_column='restrict_device_types',
        verbose_name=_('restrict device types'),
        help_text=_(
            'Flag indicating whether types of devices are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)
    restrict_event_types = models.BooleanField(
        db_column='restrict_event_types',
        verbose_name=_('restrict event types'),
        help_text=_(
            'Flag indicating whether types of events are restricted to '
            'registered ones'),
        default=True,
        null=False,
        blank=True)
    restrict_sampling_event_types = models.BooleanField(
        db_column='restrict_sampling_event_types',
        verbose_name=_('restrict sampling event types'),
        help_text=_(
            'Flag indicating whether types of sampling events are restricted '
            'to registered ones'),
        default=True,
        null=False,
        blank=True)

    site_types = models.ManyToManyField(
        'SiteType',
        verbose_name=_('site types'),
        help_text=_('Types of sites valid for collections of type'),
        blank=True)
    annotation_types = models.ManyToManyField(
        'AnnotationType',
        verbose_name=_('annotation types'),
        help_text=_('Types of annotations valid for collections of type'),
        blank=True)
    licence_types = models.ManyToManyField(
        'LicenceType',
        verbose_name=_('licence types'),
        help_text=_('Types of licences valid for collections of type'),
        blank=True)
    event_types = models.ManyToManyField(
        'EventType',
        verbose_name=_('event types'),
        help_text=_('Types of events valid for collections of type'),
        blank=True)
    sampling_event_types = models.ManyToManyField(
        'SamplingEventType',
        verbose_name=_('sampling event types'),
        help_text=_('Types of sampling events valid for collections of type'),
        blank=True)
    item_types = models.ManyToManyField(
        'ItemType',
        through='CollectionItemType',
        through_fields=('collection_type', 'item_type'),
        verbose_name=_('item types'),
        help_text=_('Types of items valid for collections of type'),
        blank=True)
    device_types = models.ManyToManyField(
        'DeviceType',
        through='CollectionDeviceType',
        through_fields=('collection_type', 'device_type'),
        verbose_name=_('device types'),
        help_text=_('Types of devices valid for collections of type'),
        blank=True)

    roles = models.ManyToManyField(
        'Role',
        through='CollectionRole',
        through_fields=('collection_type', 'role'),
        verbose_name=_('roles'),
        help_text=_('Roles valid for collections of type'),
        blank=True)

    class Meta:
        verbose_name = _('Collection Type')
        verbose_name_plural = _('Collection Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _(
                'Invalid collection metadata for collection of type %(type)s. '
                'Error: %(error)s')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)

    def validate_and_get_site_type(self, site_type):
        if not self.restrict_site_types:
            return

        try:
            return self.site_types.get(name=site_type)
        except self.site_types.model.DoesNotExist:
            msg = _(
                'Site type %(site_type)s is not accepted in collection of '
                'type %(col_type)s')
            params = dict(
                site_type=site_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_annotation_type(self, annotation_type):
        if not self.restrict_annotation_types:
            return

        try:
            return self.annotation_types.get(name=annotation_type)
        except self.annotation_types.model.DoesNotExist:
            msg = _(
                'Annotation type %(annotation_type)s is not accepted in '
                'collection of type %(col_type)s')
            params = dict(
                annotation_type=annotation_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_licence_type(self, licence_type):
        if not self.restrict_licence_types:
            return

        try:
            return self.licence_types.get(pk=licence_type.pk)
        except self.licence_types.model.DoesNotExist:
            msg = _(
                'Licence type %(licence_type)s is not accepted in collection '
                'of type %(col_type)s')
            params = dict(
                licence_type=licence_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_event_type(self, event_type):
        if not self.restrict_event_types:
            return

        try:
            return self.event_types.get(name=event_type)
        except self.event_types.model.DoesNotExist:
            msg = _(
                'Event type %(event_type)s is not accepted in collection of '
                'type %(col_type)s')
            params = dict(
                event_type=event_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_item_type(self, item_type):
        if not self.restrict_item_types:
            return

        try:
            return CollectionItemType.objects.get(
                collection_type=self,
                item_type=item_type)
        except CollectionItemType.DoesNotExist:
            msg = _(
                'Item type %(item_type)s is not accepted in collection of '
                'type %(col_type)s')
            params = dict(
                item_type=item_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_device_type(self, device_type):
        if not self.restrict_device_types:
            return

        try:
            return CollectionDeviceType.objects.get(
                collection_type=self,
                device_type=device_type)
        except CollectionDeviceType.DoesNotExist:
            msg = _(
                'Device type %(device_type)s is not accepted in collection of '
                'type %(col_type)s')
            params = dict(
                device_type=device_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_sampling_event_type(self, sampling_event_type):
        if not self.restrict_sampling_event_types:
            return

        try:
            return self.sampling_event_types.get(name=sampling_event_type)
        except self.sampling_event_types.model.DoesNotExist:
            msg = _(
                'Sampling Event type %(sampling_event_type)s is not accepted '
                'in collection of type %(col_type)s')
            params = dict(
                sampling_event_type=sampling_event_type,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def validate_and_get_role(self, role):
        try:
            return CollectionRole.objects.get(
                collection_type=self,
                role=role)
        except CollectionRole.DoesNotExist:
            msg = _(
                'Role type %(role)s is not accepted in collection of type '
                '%(col_type)s')
            params = dict(
                role=role,
                col_type=str(self))
            raise ValidationError(msg, params=params)

    def add_site_type(self, site_type):
        self.site_types.add(site_type)
        self.save()

    def remove_site_type(self, site_type):
        self.site_types.remove(site_type)
        self.save()

    def add_annotation_type(self, annotation_type):
        self.annotation_types.add(annotation_type)
        self.save()

    def remove_annotation_type(self, annotation_type):
        self.annotation_types.remove(annotation_type)
        self.save()

    def add_licence_type(self, licence_type):
        self.licence_types.add(licence_type)
        self.save()

    def remove_licence_type(self, licence_type):
        self.licence_types.remove(licence_type)
        self.save()

    def add_event_type(self, event_type):
        self.event_types.add(event_type)
        self.save()

    def remove_event_type(self, event_type):
        self.event_types.remove(event_type)
        self.save()

    def add_sampling_event_type(self, sampling_event_type):
        self.sampling_event_types.add(sampling_event_type)
        self.save()

    def remove_sampling_event_type(self, sampling_event_type):
        self.sampling_event_types.remove(sampling_event_type)
        self.save()

    def add_device_type(self, device_type, metadata_schema=None):
        if metadata_schema is None:
            metadata_schema = simple_JSON_schema()

        CollectionDeviceType.objects.get_or_create(
            collection_type=self,
            device_type=device_type,
            metadata_schema=metadata_schema)
        self.save()

    def remove_device_type(self, device_type):
        try:
            collection_device_type = CollectionDeviceType.objects.get(
                collection_type=self,
                device_type=device_type)
        except CollectionDeviceType.DoesNotExist as error:
            raise ValidationError(error)

        collection_device_type.delete()
        self.save()

    def add_item_type(self, item_type, metadata_schema=None):
        if metadata_schema is None:
            metadata_schema = simple_JSON_schema()

        CollectionItemType.objects.get_or_create(
            collection_type=self,
            item_type=item_type,
            metadata_schema=metadata_schema)
        self.save()

    def remove_item_type(self, item_type):
        try:
            collection_item_type = CollectionItemType.objects.get(
                collection_type=self,
                item_type=item_type)
        except CollectionItemType.DoesNotExist as error:
            raise ValidationError(error)

        collection_item_type.delete()
        self.save()

    def add_role(self, role, metadata_schema=None):
        if metadata_schema is None:
            metadata_schema = simple_JSON_schema()

        CollectionRole.objects.get_or_create(
            collection_type=self,
            role=role,
            metadata_schema=metadata_schema)
        self.save()

    def remove_role(self, role):
        try:
            collection_role = CollectionRole.objects.get(
                collection_type=self,
                role=role)
        except CollectionRole.DoesNotExist as error:
            raise ValidationError(error)

        collection_role.delete()
        self.save()

    def add_administrator(self, user):
        self.administrators.add(user)
        self.save()

    def remove_administrator(self, user):
        self.administrators.remove(user)
        self.save()

    def is_admin(self, user):
        return self.administrators.filter(id=user.id).exists()

    @property
    def users(self):
        return CollectionUser.objects.filter(
            collection__collection_type=self)

    @property
    def collections(self):
        return Collection.objects.filter(collection_type=self)

    @property
    def items(self):
        return Item.objects.filter(
            sampling_event_device__sampling_event__collection__collection_type=self
        )

    @property
    def annotations(self):
        return Annotation.objects.filter(
            item__sampling_event_device__sampling_event__collection__collection_type=self
        )

    @property
    def last_item(self):
        return Item.objects.filter(
            sampling_event_device__sampling_event__collection__collection_type=self
        ).order_by('-created_on').first()

    @property
    def last_annotation(self):
        return Annotation.objects.filter(
            item__sampling_event_device__sampling_event__collection__collection_type=self
        ).order_by('-created_on').first()
