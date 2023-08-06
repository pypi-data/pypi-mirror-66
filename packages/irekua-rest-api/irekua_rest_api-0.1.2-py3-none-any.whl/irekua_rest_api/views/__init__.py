# pylint: disable=C0301
from .annotations.annotation_tools import AnnotationToolViewSet
from .annotations.annotation_votes import AnnotationVoteViewSet
from .annotations.annotations import AnnotationViewSet
from .data_collections.collection_devices import CollectionDeviceViewSet
from .data_collections.collection_sites import CollectionSiteViewSet
from .data_collections.collection_users import CollectionUserViewSet
from .data_collections.data_collections import CollectionViewSet
from .data_collections.metacollections import MetaCollectionViewSet
from .data_collections.administrators import CollectionAdministratorViewSet
from .devices.device_brands import DeviceBrandViewSet
from .devices.devices import DeviceViewSet
from .devices.physical_devices import PhysicalDeviceViewSet
from .items.items import ItemViewSet
from .licences import LicenceViewSet
from .object_types.annotation_types import AnnotationTypeViewSet
from .object_types.data_collections.collection_administrators import CollectionTypeAdministratorViewSet
from .object_types.data_collections.collection_annotation_types import CollectionTypeAnnotationTypeViewSet
from .object_types.data_collections.collection_licence_types import CollectionTypeLicenceTypeViewSet
from .object_types.data_collections.collection_sampling_event_types import CollectionTypeSamplingEventTypeViewSet
from .object_types.data_collections.collection_site_types import CollectionTypeSiteTypeViewSet
from .object_types.data_collections.collection_event_types import CollectionTypeEventTypeViewSet
from .object_types.data_collections.collection_types import CollectionTypeViewSet
from .object_types.data_collections.collection_item_types import CollectionTypeItemTypeViewSet
from .object_types.data_collections.collection_device_types import CollectionTypeDeviceTypeViewSet
from .object_types.data_collections.collection_roles import CollectionTypeRoleViewSet
from .object_types.device_types import DeviceTypeViewSet
from .object_types.entailment_types import EntailmentTypeViewSet
from .object_types.event_types import EventTypeViewSet
from .object_types.item_types import ItemTypeViewSet
from .object_types.mime_types import MimeTypeViewSet
from .object_types.licence_types import LicenceTypeViewSet
from .object_types.sampling_events.sampling_event_type_device_types import SamplingEventTypeDeviceTypeViewSet
from .object_types.sampling_events.sampling_event_type_site_types import SamplingEventTypeSiteTypeViewSet
from .object_types.sampling_events.sampling_event_types import SamplingEventTypeViewSet
from .object_types.site_types import SiteTypeViewSet
from .object_types.term_types import TermTypeViewSet
from .sampling_events.sampling_event_devices import SamplingEventDeviceViewSet
from .sampling_events.sampling_events import SamplingEventViewSet
from .items.secondary_items import SecondaryItemViewSet
from .sites import SiteViewSet
from .items.tags import TagViewSet
from .terms.entailments import EntailmentViewSet
from .terms.synonym_suggestions import SynonymSuggestionViewSet
from .terms.synonyms import SynonymViewSet
from .terms.term_suggestions import TermSuggestionViewSet
from .terms.terms import TermViewSet
from .users.institutions import InstitutionViewSet
from .users.roles import RoleViewSet
from .users.users import UserViewSet
from .models.model import ModelViewSet
from .models.model_version import ModelVersionViewSet
from .models.model_prediction import ModelPredictionViewSet


__all__ = [
    'AnnotationToolViewSet',
    'AnnotationTypeViewSet',
    'AnnotationViewSet',
    'AnnotationVoteViewSet',
    'CollectionDeviceViewSet',
    'CollectionSiteViewSet',
    'CollectionTypeAdministratorViewSet',
    'CollectionTypeAnnotationTypeViewSet',
    'CollectionTypeLicenceTypeViewSet',
    'CollectionTypeSamplingEventTypeViewSet',
    'CollectionTypeItemTypeViewSet',
    'CollectionTypeSiteTypeViewSet',
    'CollectionTypeEventTypeViewSet',
    'CollectionTypeViewSet',
    'CollectionUserViewSet',
    'CollectionViewSet',
    'DeviceBrandViewSet',
    'DeviceTypeViewSet',
    'DeviceViewSet',
    'EntailmentTypeViewSet',
    'EntailmentViewSet',
    'EventTypeViewSet',
    'InstitutionViewSet',
    'ItemTypeViewSet',
    'ItemViewSet',
    'LicenceTypeViewSet',
    'LicenceViewSet',
    'MetaCollectionViewSet',
    'PhysicalDeviceViewSet',
    'RoleViewSet',
    'SamplingEventDeviceViewSet',
    'SamplingEventTypeDeviceTypeViewSet',
    'SamplingEventTypeSiteTypeViewSet',
    'SamplingEventTypeViewSet',
    'SamplingEventViewSet',
    'SecondaryItemViewSet',
    'SiteTypeViewSet',
    'SiteViewSet',
    'SynonymSuggestionViewSet',
    'SynonymViewSet',
    'TagViewSet',
    'TermSuggestionViewSet',
    'TermTypeViewSet',
    'TermViewSet',
    'UserViewSet',
    'CollectionTypeDeviceTypeViewSet',
    'CollectionTypeRoleViewSet',
    'CollectionAdministratorViewSet',
    'MimeTypeViewSet',
    'ModelViewSet',
    'ModelVersionViewSet',
    'ModelPredictionViewSet'
]
