# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/services/customer_client_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v1.proto.resources import customer_client_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_customer__client__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/services/customer_client_service.proto',
  package='google.ads.googleads.v1.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v1.servicesB\032CustomerClientServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V1.Services\312\002 Google\\Ads\\GoogleAds\\V1\\Services\352\002$Google::Ads::GoogleAds::V1::Services'),
  serialized_pb=_b('\nDgoogle/ads/googleads_v1/proto/services/customer_client_service.proto\x12 google.ads.googleads.v1.services\x1a=google/ads/googleads_v1/proto/resources/customer_client.proto\x1a\x1cgoogle/api/annotations.proto\"1\n\x18GetCustomerClientRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xd7\x01\n\x15\x43ustomerClientService\x12\xbd\x01\n\x11GetCustomerClient\x12:.google.ads.googleads.v1.services.GetCustomerClientRequest\x1a\x31.google.ads.googleads.v1.resources.CustomerClient\"9\x82\xd3\xe4\x93\x02\x33\x12\x31/v1/{resource_name=customers/*/customerClients/*}B\x81\x02\n$com.google.ads.googleads.v1.servicesB\x1a\x43ustomerClientServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V1.Services\xca\x02 Google\\Ads\\GoogleAds\\V1\\Services\xea\x02$Google::Ads::GoogleAds::V1::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_customer__client__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_GETCUSTOMERCLIENTREQUEST = _descriptor.Descriptor(
  name='GetCustomerClientRequest',
  full_name='google.ads.googleads.v1.services.GetCustomerClientRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.services.GetCustomerClientRequest.resource_name', index=0,
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
  serialized_start=199,
  serialized_end=248,
)

DESCRIPTOR.message_types_by_name['GetCustomerClientRequest'] = _GETCUSTOMERCLIENTREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetCustomerClientRequest = _reflection.GeneratedProtocolMessageType('GetCustomerClientRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETCUSTOMERCLIENTREQUEST,
  __module__ = 'google.ads.googleads_v1.proto.services.customer_client_service_pb2'
  ,
  __doc__ = """Request message for
  [CustomerClientService.GetCustomerClient][google.ads.googleads.v1.services.CustomerClientService.GetCustomerClient].
  
  
  Attributes:
      resource_name:
          The resource name of the client to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.GetCustomerClientRequest)
  ))
_sym_db.RegisterMessage(GetCustomerClientRequest)


DESCRIPTOR._options = None

_CUSTOMERCLIENTSERVICE = _descriptor.ServiceDescriptor(
  name='CustomerClientService',
  full_name='google.ads.googleads.v1.services.CustomerClientService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=251,
  serialized_end=466,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetCustomerClient',
    full_name='google.ads.googleads.v1.services.CustomerClientService.GetCustomerClient',
    index=0,
    containing_service=None,
    input_type=_GETCUSTOMERCLIENTREQUEST,
    output_type=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_customer__client__pb2._CUSTOMERCLIENT,
    serialized_options=_b('\202\323\344\223\0023\0221/v1/{resource_name=customers/*/customerClients/*}'),
  ),
])
_sym_db.RegisterServiceDescriptor(_CUSTOMERCLIENTSERVICE)

DESCRIPTOR.services_by_name['CustomerClientService'] = _CUSTOMERCLIENTSERVICE

# @@protoc_insertion_point(module_scope)
