# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/services/group_placement_view_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v1.proto.resources import group_placement_view_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_group__placement__view__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/services/group_placement_view_service.proto',
  package='google.ads.googleads.v1.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v1.servicesB\036GroupPlacementViewServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V1.Services\312\002 Google\\Ads\\GoogleAds\\V1\\Services\352\002$Google::Ads::GoogleAds::V1::Services'),
  serialized_pb=_b('\nIgoogle/ads/googleads_v1/proto/services/group_placement_view_service.proto\x12 google.ads.googleads.v1.services\x1a\x42google/ads/googleads_v1/proto/resources/group_placement_view.proto\x1a\x1cgoogle/api/annotations.proto\"5\n\x1cGetGroupPlacementViewRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xeb\x01\n\x19GroupPlacementViewService\x12\xcd\x01\n\x15GetGroupPlacementView\x12>.google.ads.googleads.v1.services.GetGroupPlacementViewRequest\x1a\x35.google.ads.googleads.v1.resources.GroupPlacementView\"=\x82\xd3\xe4\x93\x02\x37\x12\x35/v1/{resource_name=customers/*/groupPlacementViews/*}B\x85\x02\n$com.google.ads.googleads.v1.servicesB\x1eGroupPlacementViewServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V1.Services\xca\x02 Google\\Ads\\GoogleAds\\V1\\Services\xea\x02$Google::Ads::GoogleAds::V1::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_group__placement__view__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_GETGROUPPLACEMENTVIEWREQUEST = _descriptor.Descriptor(
  name='GetGroupPlacementViewRequest',
  full_name='google.ads.googleads.v1.services.GetGroupPlacementViewRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.services.GetGroupPlacementViewRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=209,
  serialized_end=262,
)

DESCRIPTOR.message_types_by_name['GetGroupPlacementViewRequest'] = _GETGROUPPLACEMENTVIEWREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetGroupPlacementViewRequest = _reflection.GeneratedProtocolMessageType('GetGroupPlacementViewRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETGROUPPLACEMENTVIEWREQUEST,
  __module__ = 'google.ads.googleads_v1.proto.services.group_placement_view_service_pb2'
  ,
  __doc__ = """Request message for
  [GroupPlacementViewService.GetGroupPlacementView][google.ads.googleads.v1.services.GroupPlacementViewService.GetGroupPlacementView].
  
  
  Attributes:
      resource_name:
          The resource name of the Group Placement view to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.GetGroupPlacementViewRequest)
  ))
_sym_db.RegisterMessage(GetGroupPlacementViewRequest)


DESCRIPTOR._options = None

_GROUPPLACEMENTVIEWSERVICE = _descriptor.ServiceDescriptor(
  name='GroupPlacementViewService',
  full_name='google.ads.googleads.v1.services.GroupPlacementViewService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=265,
  serialized_end=500,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetGroupPlacementView',
    full_name='google.ads.googleads.v1.services.GroupPlacementViewService.GetGroupPlacementView',
    index=0,
    containing_service=None,
    input_type=_GETGROUPPLACEMENTVIEWREQUEST,
    output_type=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_group__placement__view__pb2._GROUPPLACEMENTVIEW,
    serialized_options=_b('\202\323\344\223\0027\0225/v1/{resource_name=customers/*/groupPlacementViews/*}'),
  ),
])
_sym_db.RegisterServiceDescriptor(_GROUPPLACEMENTVIEWSERVICE)

DESCRIPTOR.services_by_name['GroupPlacementViewService'] = _GROUPPLACEMENTVIEWSERVICE

# @@protoc_insertion_point(module_scope)
