# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/resources/group_placement_view.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v3.proto.enums import placement_type_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_placement__type__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/resources/group_placement_view.proto',
  package='google.ads.googleads.v3.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v3.resourcesB\027GroupPlacementViewProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V3.Resources\312\002!Google\\Ads\\GoogleAds\\V3\\Resources\352\002%Google::Ads::GoogleAds::V3::Resources'),
  serialized_pb=_b('\nBgoogle/ads/googleads_v3/proto/resources/group_placement_view.proto\x12!google.ads.googleads.v3.resources\x1a\x38google/ads/googleads_v3/proto/enums/placement_type.proto\x1a\x19google/api/resource.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\x8d\x03\n\x12GroupPlacementView\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12/\n\tplacement\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x32\n\x0c\x64isplay_name\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x30\n\ntarget_url\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12V\n\x0eplacement_type\x18\x05 \x01(\x0e\x32>.google.ads.googleads.v3.enums.PlacementTypeEnum.PlacementType:q\xea\x41n\n+googleads.googleapis.com/GroupPlacementView\x12?customers/{customer}/groupPlacementViews/{group_placement_view}B\x84\x02\n%com.google.ads.googleads.v3.resourcesB\x17GroupPlacementViewProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V3.Resources\xca\x02!Google\\Ads\\GoogleAds\\V3\\Resources\xea\x02%Google::Ads::GoogleAds::V3::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_placement__type__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_GROUPPLACEMENTVIEW = _descriptor.Descriptor(
  name='GroupPlacementView',
  full_name='google.ads.googleads.v3.resources.GroupPlacementView',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.resources.GroupPlacementView.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='placement', full_name='google.ads.googleads.v3.resources.GroupPlacementView.placement', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='display_name', full_name='google.ads.googleads.v3.resources.GroupPlacementView.display_name', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target_url', full_name='google.ads.googleads.v3.resources.GroupPlacementView.target_url', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='placement_type', full_name='google.ads.googleads.v3.resources.GroupPlacementView.placement_type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\352An\n+googleads.googleapis.com/GroupPlacementView\022?customers/{customer}/groupPlacementViews/{group_placement_view}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=253,
  serialized_end=650,
)

_GROUPPLACEMENTVIEW.fields_by_name['placement'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GROUPPLACEMENTVIEW.fields_by_name['display_name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GROUPPLACEMENTVIEW.fields_by_name['target_url'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GROUPPLACEMENTVIEW.fields_by_name['placement_type'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_placement__type__pb2._PLACEMENTTYPEENUM_PLACEMENTTYPE
DESCRIPTOR.message_types_by_name['GroupPlacementView'] = _GROUPPLACEMENTVIEW
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GroupPlacementView = _reflection.GeneratedProtocolMessageType('GroupPlacementView', (_message.Message,), dict(
  DESCRIPTOR = _GROUPPLACEMENTVIEW,
  __module__ = 'google.ads.googleads_v3.proto.resources.group_placement_view_pb2'
  ,
  __doc__ = """A group placement view.
  
  
  Attributes:
      resource_name:
          The resource name of the group placement view. Group placement
          view resource names have the form:  ``customers/{customer_id}/
          groupPlacementViews/{ad_group_id}~{base64_placement}``
      placement:
          The automatic placement string at group level, e. g. web
          domain, mobile app ID, or a YouTube channel ID.
      display_name:
          Domain name for websites and YouTube channel name for YouTube
          channels.
      target_url:
          URL of the group placement, e.g. domain, link to the mobile
          application in app store, or a YouTube channel URL.
      placement_type:
          Type of the placement, e.g. Website, YouTube Channel, Mobile
          Application.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.resources.GroupPlacementView)
  ))
_sym_db.RegisterMessage(GroupPlacementView)


DESCRIPTOR._options = None
_GROUPPLACEMENTVIEW._options = None
# @@protoc_insertion_point(module_scope)
