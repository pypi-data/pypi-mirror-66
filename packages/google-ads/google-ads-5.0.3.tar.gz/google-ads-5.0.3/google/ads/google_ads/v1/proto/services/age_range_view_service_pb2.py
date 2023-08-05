# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/services/age_range_view_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v1.proto.resources import age_range_view_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_age__range__view__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/services/age_range_view_service.proto',
  package='google.ads.googleads.v1.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v1.servicesB\030AgeRangeViewServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V1.Services\312\002 Google\\Ads\\GoogleAds\\V1\\Services\352\002$Google::Ads::GoogleAds::V1::Services'),
  serialized_pb=_b('\nCgoogle/ads/googleads_v1/proto/services/age_range_view_service.proto\x12 google.ads.googleads.v1.services\x1a<google/ads/googleads_v1/proto/resources/age_range_view.proto\x1a\x1cgoogle/api/annotations.proto\"/\n\x16GetAgeRangeViewRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xcd\x01\n\x13\x41geRangeViewService\x12\xb5\x01\n\x0fGetAgeRangeView\x12\x38.google.ads.googleads.v1.services.GetAgeRangeViewRequest\x1a/.google.ads.googleads.v1.resources.AgeRangeView\"7\x82\xd3\xe4\x93\x02\x31\x12//v1/{resource_name=customers/*/ageRangeViews/*}B\xff\x01\n$com.google.ads.googleads.v1.servicesB\x18\x41geRangeViewServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V1.Services\xca\x02 Google\\Ads\\GoogleAds\\V1\\Services\xea\x02$Google::Ads::GoogleAds::V1::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_age__range__view__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_GETAGERANGEVIEWREQUEST = _descriptor.Descriptor(
  name='GetAgeRangeViewRequest',
  full_name='google.ads.googleads.v1.services.GetAgeRangeViewRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.services.GetAgeRangeViewRequest.resource_name', index=0,
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
  serialized_start=197,
  serialized_end=244,
)

DESCRIPTOR.message_types_by_name['GetAgeRangeViewRequest'] = _GETAGERANGEVIEWREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAgeRangeViewRequest = _reflection.GeneratedProtocolMessageType('GetAgeRangeViewRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETAGERANGEVIEWREQUEST,
  __module__ = 'google.ads.googleads_v1.proto.services.age_range_view_service_pb2'
  ,
  __doc__ = """Request message for
  [AgeRangeViewService.GetAgeRangeView][google.ads.googleads.v1.services.AgeRangeViewService.GetAgeRangeView].
  
  
  Attributes:
      resource_name:
          The resource name of the age range view to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.GetAgeRangeViewRequest)
  ))
_sym_db.RegisterMessage(GetAgeRangeViewRequest)


DESCRIPTOR._options = None

_AGERANGEVIEWSERVICE = _descriptor.ServiceDescriptor(
  name='AgeRangeViewService',
  full_name='google.ads.googleads.v1.services.AgeRangeViewService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=247,
  serialized_end=452,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAgeRangeView',
    full_name='google.ads.googleads.v1.services.AgeRangeViewService.GetAgeRangeView',
    index=0,
    containing_service=None,
    input_type=_GETAGERANGEVIEWREQUEST,
    output_type=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_age__range__view__pb2._AGERANGEVIEW,
    serialized_options=_b('\202\323\344\223\0021\022//v1/{resource_name=customers/*/ageRangeViews/*}'),
  ),
])
_sym_db.RegisterServiceDescriptor(_AGERANGEVIEWSERVICE)

DESCRIPTOR.services_by_name['AgeRangeViewService'] = _AGERANGEVIEWSERVICE

# @@protoc_insertion_point(module_scope)
