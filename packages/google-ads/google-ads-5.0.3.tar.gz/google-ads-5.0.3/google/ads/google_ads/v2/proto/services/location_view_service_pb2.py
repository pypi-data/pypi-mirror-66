# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/services/location_view_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v2.proto.resources import location_view_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_location__view__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v2/proto/services/location_view_service.proto',
  package='google.ads.googleads.v2.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v2.servicesB\030LocationViewServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v2/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V2.Services\312\002 Google\\Ads\\GoogleAds\\V2\\Services\352\002$Google::Ads::GoogleAds::V2::Services'),
  serialized_pb=_b('\nBgoogle/ads/googleads_v2/proto/services/location_view_service.proto\x12 google.ads.googleads.v2.services\x1a;google/ads/googleads_v2/proto/resources/location_view.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\"/\n\x16GetLocationViewRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xea\x01\n\x13LocationViewService\x12\xb5\x01\n\x0fGetLocationView\x12\x38.google.ads.googleads.v2.services.GetLocationViewRequest\x1a/.google.ads.googleads.v2.resources.LocationView\"7\x82\xd3\xe4\x93\x02\x31\x12//v2/{resource_name=customers/*/locationViews/*}\x1a\x1b\xca\x41\x18googleads.googleapis.comB\xff\x01\n$com.google.ads.googleads.v2.servicesB\x18LocationViewServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v2/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V2.Services\xca\x02 Google\\Ads\\GoogleAds\\V2\\Services\xea\x02$Google::Ads::GoogleAds::V2::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_location__view__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,])




_GETLOCATIONVIEWREQUEST = _descriptor.Descriptor(
  name='GetLocationViewRequest',
  full_name='google.ads.googleads.v2.services.GetLocationViewRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.services.GetLocationViewRequest.resource_name', index=0,
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
  serialized_start=220,
  serialized_end=267,
)

DESCRIPTOR.message_types_by_name['GetLocationViewRequest'] = _GETLOCATIONVIEWREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetLocationViewRequest = _reflection.GeneratedProtocolMessageType('GetLocationViewRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETLOCATIONVIEWREQUEST,
  __module__ = 'google.ads.googleads_v2.proto.services.location_view_service_pb2'
  ,
  __doc__ = """Request message for
  [LocationViewService.GetLocationView][google.ads.googleads.v2.services.LocationViewService.GetLocationView].
  
  
  Attributes:
      resource_name:
          The resource name of the location view to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.GetLocationViewRequest)
  ))
_sym_db.RegisterMessage(GetLocationViewRequest)


DESCRIPTOR._options = None

_LOCATIONVIEWSERVICE = _descriptor.ServiceDescriptor(
  name='LocationViewService',
  full_name='google.ads.googleads.v2.services.LocationViewService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=270,
  serialized_end=504,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetLocationView',
    full_name='google.ads.googleads.v2.services.LocationViewService.GetLocationView',
    index=0,
    containing_service=None,
    input_type=_GETLOCATIONVIEWREQUEST,
    output_type=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_location__view__pb2._LOCATIONVIEW,
    serialized_options=_b('\202\323\344\223\0021\022//v2/{resource_name=customers/*/locationViews/*}'),
  ),
])
_sym_db.RegisterServiceDescriptor(_LOCATIONVIEWSERVICE)

DESCRIPTOR.services_by_name['LocationViewService'] = _LOCATIONVIEWSERVICE

# @@protoc_insertion_point(module_scope)
