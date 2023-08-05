# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/resources/gender_view.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/resources/gender_view.proto',
  package='google.ads.googleads.v1.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v1.resourcesB\017GenderViewProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v1/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V1.Resources\312\002!Google\\Ads\\GoogleAds\\V1\\Resources\352\002%Google::Ads::GoogleAds::V1::Resources'),
  serialized_pb=_b('\n9google/ads/googleads_v1/proto/resources/gender_view.proto\x12!google.ads.googleads.v1.resources\x1a\x1cgoogle/api/annotations.proto\"#\n\nGenderView\x12\x15\n\rresource_name\x18\x01 \x01(\tB\xfc\x01\n%com.google.ads.googleads.v1.resourcesB\x0fGenderViewProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v1/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V1.Resources\xca\x02!Google\\Ads\\GoogleAds\\V1\\Resources\xea\x02%Google::Ads::GoogleAds::V1::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_GENDERVIEW = _descriptor.Descriptor(
  name='GenderView',
  full_name='google.ads.googleads.v1.resources.GenderView',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.resources.GenderView.resource_name', index=0,
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
  serialized_start=126,
  serialized_end=161,
)

DESCRIPTOR.message_types_by_name['GenderView'] = _GENDERVIEW
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GenderView = _reflection.GeneratedProtocolMessageType('GenderView', (_message.Message,), dict(
  DESCRIPTOR = _GENDERVIEW,
  __module__ = 'google.ads.googleads_v1.proto.resources.gender_view_pb2'
  ,
  __doc__ = """A gender view.
  
  
  Attributes:
      resource_name:
          The resource name of the gender view. Gender view resource
          names have the form:  ``customers/{customer_id}/genderViews/{a
          d_group_id}~{criterion_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.resources.GenderView)
  ))
_sym_db.RegisterMessage(GenderView)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
