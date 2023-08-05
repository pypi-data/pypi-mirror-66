# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/services/video_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v2.proto.resources import video_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_video__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v2/proto/services/video_service.proto',
  package='google.ads.googleads.v2.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v2.servicesB\021VideoServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v2/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V2.Services\312\002 Google\\Ads\\GoogleAds\\V2\\Services\352\002$Google::Ads::GoogleAds::V2::Services'),
  serialized_pb=_b('\n:google/ads/googleads_v2/proto/services/video_service.proto\x12 google.ads.googleads.v2.services\x1a\x33google/ads/googleads_v2/proto/resources/video.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\"(\n\x0fGetVideoRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xc7\x01\n\x0cVideoService\x12\x99\x01\n\x08GetVideo\x12\x31.google.ads.googleads.v2.services.GetVideoRequest\x1a(.google.ads.googleads.v2.resources.Video\"0\x82\xd3\xe4\x93\x02*\x12(/v2/{resource_name=customers/*/videos/*}\x1a\x1b\xca\x41\x18googleads.googleapis.comB\xf8\x01\n$com.google.ads.googleads.v2.servicesB\x11VideoServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v2/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V2.Services\xca\x02 Google\\Ads\\GoogleAds\\V2\\Services\xea\x02$Google::Ads::GoogleAds::V2::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_video__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,])




_GETVIDEOREQUEST = _descriptor.Descriptor(
  name='GetVideoRequest',
  full_name='google.ads.googleads.v2.services.GetVideoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.services.GetVideoRequest.resource_name', index=0,
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
  serialized_start=204,
  serialized_end=244,
)

DESCRIPTOR.message_types_by_name['GetVideoRequest'] = _GETVIDEOREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetVideoRequest = _reflection.GeneratedProtocolMessageType('GetVideoRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETVIDEOREQUEST,
  __module__ = 'google.ads.googleads_v2.proto.services.video_service_pb2'
  ,
  __doc__ = """Request message for
  [VideoService.GetVideo][google.ads.googleads.v2.services.VideoService.GetVideo].
  
  
  Attributes:
      resource_name:
          The resource name of the video to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.GetVideoRequest)
  ))
_sym_db.RegisterMessage(GetVideoRequest)


DESCRIPTOR._options = None

_VIDEOSERVICE = _descriptor.ServiceDescriptor(
  name='VideoService',
  full_name='google.ads.googleads.v2.services.VideoService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=247,
  serialized_end=446,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetVideo',
    full_name='google.ads.googleads.v2.services.VideoService.GetVideo',
    index=0,
    containing_service=None,
    input_type=_GETVIDEOREQUEST,
    output_type=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_video__pb2._VIDEO,
    serialized_options=_b('\202\323\344\223\002*\022(/v2/{resource_name=customers/*/videos/*}'),
  ),
])
_sym_db.RegisterServiceDescriptor(_VIDEOSERVICE)

DESCRIPTOR.services_by_name['VideoService'] = _VIDEOSERVICE

# @@protoc_insertion_point(module_scope)
