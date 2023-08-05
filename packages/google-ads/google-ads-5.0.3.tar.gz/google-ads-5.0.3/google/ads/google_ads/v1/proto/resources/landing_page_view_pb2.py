# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/resources/landing_page_view.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/resources/landing_page_view.proto',
  package='google.ads.googleads.v1.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v1.resourcesB\024LandingPageViewProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v1/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V1.Resources\312\002!Google\\Ads\\GoogleAds\\V1\\Resources\352\002%Google::Ads::GoogleAds::V1::Resources'),
  serialized_pb=_b('\n?google/ads/googleads_v1/proto/resources/landing_page_view.proto\x12!google.ads.googleads.v1.resources\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"d\n\x0fLandingPageView\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12:\n\x14unexpanded_final_url\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x81\x02\n%com.google.ads.googleads.v1.resourcesB\x14LandingPageViewProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v1/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V1.Resources\xca\x02!Google\\Ads\\GoogleAds\\V1\\Resources\xea\x02%Google::Ads::GoogleAds::V1::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_LANDINGPAGEVIEW = _descriptor.Descriptor(
  name='LandingPageView',
  full_name='google.ads.googleads.v1.resources.LandingPageView',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.resources.LandingPageView.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unexpanded_final_url', full_name='google.ads.googleads.v1.resources.LandingPageView.unexpanded_final_url', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=164,
  serialized_end=264,
)

_LANDINGPAGEVIEW.fields_by_name['unexpanded_final_url'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['LandingPageView'] = _LANDINGPAGEVIEW
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LandingPageView = _reflection.GeneratedProtocolMessageType('LandingPageView', (_message.Message,), dict(
  DESCRIPTOR = _LANDINGPAGEVIEW,
  __module__ = 'google.ads.googleads_v1.proto.resources.landing_page_view_pb2'
  ,
  __doc__ = """A landing page view with metrics aggregated at the unexpanded final URL
  level.
  
  
  Attributes:
      resource_name:
          The resource name of the landing page view. Landing page view
          resource names have the form:  ``customers/{customer_id}/landi
          ngPageViews/{unexpanded_final_url_fingerprint}``
      unexpanded_final_url:
          The advertiser-specified final URL.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.resources.LandingPageView)
  ))
_sym_db.RegisterMessage(LandingPageView)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
