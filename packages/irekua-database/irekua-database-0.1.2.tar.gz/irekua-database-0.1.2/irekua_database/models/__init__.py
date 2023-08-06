from django.contrib.auth.models import Group

from .annotations.annotation_tools import AnnotationTool
from .annotations.annotation_votes import AnnotationVote
from .annotations.annotations import Annotation
from .data_collections.collection_devices import CollectionDevice
from .data_collections.collection_sites import CollectionSite
from .data_collections.collection_users import CollectionUser
from .data_collections.data_collections import Collection
from .data_collections.metacollections import MetaCollection
from .devices.device_brands import DeviceBrand
from .devices.devices import Device
from .devices.physical_devices import PhysicalDevice
from .items.items import Item
from .items.secondary_items import SecondaryItem
from .items.sources import Source
from .items.tags import Tag
from .licences import Licence
from .object_types.annotation_types import AnnotationType
from .object_types.data_collections.collection_device_types import CollectionDeviceType
from .object_types.data_collections.collection_item_types import CollectionItemType
from .object_types.data_collections.collection_roles import CollectionRole
from .object_types.data_collections.collection_types import CollectionType
from .object_types.device_types import DeviceType
from .object_types.entailment_types import EntailmentType
from .object_types.event_types import EventType
from .object_types.item_types import ItemType
from .object_types.licence_types import LicenceType
from .object_types.locality_types import LocalityType
from .object_types.mime_types import MimeType
from .object_types.sampling_events.sampling_event_type_devices import SamplingEventTypeDeviceType
from .object_types.sampling_events.sampling_event_types import SamplingEventType
from .object_types.site_descriptor_types import SiteDescriptorType
from .object_types.site_types import SiteType
from .object_types.term_types import TermType
from .sampling_events.sampling_event_devices import SamplingEventDevice
from .sampling_events.sampling_events import SamplingEvent
from .sites.localities import Locality
from .sites.site_descriptors import SiteDescriptor
from .sites.sites import Site
from .terms.entailments import Entailment
from .terms.synonym_suggestions import SynonymSuggestion
from .terms.synonyms import Synonym
from .terms.term_suggestions import TermSuggestion
from .terms.terms import Term
from .users.institutions import Institution
from .users.roles import Role
from .users.users import User
from .visualizers import Visualizer


__all__ = [
    'Annotation',
    'AnnotationTool',
    'AnnotationType',
    'AnnotationVote',
    'Collection',
    'CollectionDevice',
    'CollectionDeviceType',
    'CollectionItemType',
    'CollectionRole',
    'CollectionSite',
    'CollectionType',
    'CollectionUser',
    'Device',
    'DeviceBrand',
    'DeviceType',
    'Entailment',
    'EntailmentType',
    'EventType',
    'Group',
    'Institution',
    'Item',
    'ItemType',
    'Licence',
    'LicenceType',
    'Locality',
    'LocalityType',
    'MetaCollection',
    'MimeType',
    'PhysicalDevice',
    'Role',
    'SamplingEvent',
    'SamplingEventDevice',
    'SamplingEventType',
    'SamplingEventTypeDeviceType',
    'SecondaryItem',
    'Site',
    'SiteDescriptor',
    'SiteDescriptorType',
    'SiteType',
    'Source',
    'Synonym',
    'SynonymSuggestion',
    'Tag',
    'Term',
    'TermSuggestion',
    'TermType',
    'User',
    'Visualizer',
]
