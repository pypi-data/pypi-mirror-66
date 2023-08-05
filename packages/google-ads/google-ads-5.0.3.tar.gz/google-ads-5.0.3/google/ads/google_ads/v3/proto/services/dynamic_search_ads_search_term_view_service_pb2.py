# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/services/dynamic_search_ads_search_term_view_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v3.proto.resources import dynamic_search_ads_search_term_view_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_dynamic__search__ads__search__term__view__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/services/dynamic_search_ads_search_term_view_service.proto',
  package='google.ads.googleads.v3.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v3.servicesB*DynamicSearchAdsSearchTermViewServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v3/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V3.Services\312\002 Google\\Ads\\GoogleAds\\V3\\Services\352\002$Google::Ads::GoogleAds::V3::Services'),
  serialized_pb=_b('\nXgoogle/ads/googleads_v3/proto/services/dynamic_search_ads_search_term_view_service.proto\x12 google.ads.googleads.v3.services\x1aQgoogle/ads/googleads_v3/proto/resources/dynamic_search_ads_search_term_view.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\"F\n(GetDynamicSearchAdsSearchTermViewRequest\x12\x1a\n\rresource_name\x18\x01 \x01(\tB\x03\xe0\x41\x02\x32\xd4\x02\n%DynamicSearchAdsSearchTermViewService\x12\x8d\x02\n!GetDynamicSearchAdsSearchTermView\x12J.google.ads.googleads.v3.services.GetDynamicSearchAdsSearchTermViewRequest\x1a\x41.google.ads.googleads.v3.resources.DynamicSearchAdsSearchTermView\"Y\x82\xd3\xe4\x93\x02\x43\x12\x41/v3/{resource_name=customers/*/dynamicSearchAdsSearchTermViews/*}\xda\x41\rresource_name\x1a\x1b\xca\x41\x18googleads.googleapis.comB\x91\x02\n$com.google.ads.googleads.v3.servicesB*DynamicSearchAdsSearchTermViewServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v3/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V3.Services\xca\x02 Google\\Ads\\GoogleAds\\V3\\Services\xea\x02$Google::Ads::GoogleAds::V3::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_dynamic__search__ads__search__term__view__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,])




_GETDYNAMICSEARCHADSSEARCHTERMVIEWREQUEST = _descriptor.Descriptor(
  name='GetDynamicSearchAdsSearchTermViewRequest',
  full_name='google.ads.googleads.v3.services.GetDynamicSearchAdsSearchTermViewRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.services.GetDynamicSearchAdsSearchTermViewRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002'), file=DESCRIPTOR),
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
  serialized_start=297,
  serialized_end=367,
)

DESCRIPTOR.message_types_by_name['GetDynamicSearchAdsSearchTermViewRequest'] = _GETDYNAMICSEARCHADSSEARCHTERMVIEWREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetDynamicSearchAdsSearchTermViewRequest = _reflection.GeneratedProtocolMessageType('GetDynamicSearchAdsSearchTermViewRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETDYNAMICSEARCHADSSEARCHTERMVIEWREQUEST,
  __module__ = 'google.ads.googleads_v3.proto.services.dynamic_search_ads_search_term_view_service_pb2'
  ,
  __doc__ = """Request message for
  [DynamicSearchAdsSearchTermViewService.GetDynamicSearchAdsSearchTermView][google.ads.googleads.v3.services.DynamicSearchAdsSearchTermViewService.GetDynamicSearchAdsSearchTermView].
  
  
  Attributes:
      resource_name:
          Required. The resource name of the dynamic search ads search
          term view to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.GetDynamicSearchAdsSearchTermViewRequest)
  ))
_sym_db.RegisterMessage(GetDynamicSearchAdsSearchTermViewRequest)


DESCRIPTOR._options = None
_GETDYNAMICSEARCHADSSEARCHTERMVIEWREQUEST.fields_by_name['resource_name']._options = None

_DYNAMICSEARCHADSSEARCHTERMVIEWSERVICE = _descriptor.ServiceDescriptor(
  name='DynamicSearchAdsSearchTermViewService',
  full_name='google.ads.googleads.v3.services.DynamicSearchAdsSearchTermViewService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=370,
  serialized_end=710,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetDynamicSearchAdsSearchTermView',
    full_name='google.ads.googleads.v3.services.DynamicSearchAdsSearchTermViewService.GetDynamicSearchAdsSearchTermView',
    index=0,
    containing_service=None,
    input_type=_GETDYNAMICSEARCHADSSEARCHTERMVIEWREQUEST,
    output_type=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_dynamic__search__ads__search__term__view__pb2._DYNAMICSEARCHADSSEARCHTERMVIEW,
    serialized_options=_b('\202\323\344\223\002C\022A/v3/{resource_name=customers/*/dynamicSearchAdsSearchTermViews/*}\332A\rresource_name'),
  ),
])
_sym_db.RegisterServiceDescriptor(_DYNAMICSEARCHADSSEARCHTERMVIEWSERVICE)

DESCRIPTOR.services_by_name['DynamicSearchAdsSearchTermViewService'] = _DYNAMICSEARCHADSSEARCHTERMVIEWSERVICE

# @@protoc_insertion_point(module_scope)
