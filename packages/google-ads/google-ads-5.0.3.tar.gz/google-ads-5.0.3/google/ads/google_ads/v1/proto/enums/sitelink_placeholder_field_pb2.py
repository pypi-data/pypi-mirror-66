# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/enums/sitelink_placeholder_field.proto

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
  name='google/ads/googleads_v1/proto/enums/sitelink_placeholder_field.proto',
  package='google.ads.googleads.v1.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v1.enumsB\035SitelinkPlaceholderFieldProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V1.Enums\312\002\035Google\\Ads\\GoogleAds\\V1\\Enums\352\002!Google::Ads::GoogleAds::V1::Enums'),
  serialized_pb=_b('\nDgoogle/ads/googleads_v1/proto/enums/sitelink_placeholder_field.proto\x12\x1dgoogle.ads.googleads.v1.enums\x1a\x1cgoogle/api/annotations.proto\"\xca\x01\n\x1cSitelinkPlaceholderFieldEnum\"\xa9\x01\n\x18SitelinkPlaceholderField\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x08\n\x04TEXT\x10\x02\x12\n\n\x06LINE_1\x10\x03\x12\n\n\x06LINE_2\x10\x04\x12\x0e\n\nFINAL_URLS\x10\x05\x12\x15\n\x11\x46INAL_MOBILE_URLS\x10\x06\x12\x10\n\x0cTRACKING_URL\x10\x07\x12\x14\n\x10\x46INAL_URL_SUFFIX\x10\x08\x42\xf2\x01\n!com.google.ads.googleads.v1.enumsB\x1dSitelinkPlaceholderFieldProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V1.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V1\\Enums\xea\x02!Google::Ads::GoogleAds::V1::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_SITELINKPLACEHOLDERFIELDENUM_SITELINKPLACEHOLDERFIELD = _descriptor.EnumDescriptor(
  name='SitelinkPlaceholderField',
  full_name='google.ads.googleads.v1.enums.SitelinkPlaceholderFieldEnum.SitelinkPlaceholderField',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TEXT', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LINE_1', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LINE_2', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FINAL_URLS', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FINAL_MOBILE_URLS', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRACKING_URL', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FINAL_URL_SUFFIX', index=8, number=8,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=167,
  serialized_end=336,
)
_sym_db.RegisterEnumDescriptor(_SITELINKPLACEHOLDERFIELDENUM_SITELINKPLACEHOLDERFIELD)


_SITELINKPLACEHOLDERFIELDENUM = _descriptor.Descriptor(
  name='SitelinkPlaceholderFieldEnum',
  full_name='google.ads.googleads.v1.enums.SitelinkPlaceholderFieldEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SITELINKPLACEHOLDERFIELDENUM_SITELINKPLACEHOLDERFIELD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=134,
  serialized_end=336,
)

_SITELINKPLACEHOLDERFIELDENUM_SITELINKPLACEHOLDERFIELD.containing_type = _SITELINKPLACEHOLDERFIELDENUM
DESCRIPTOR.message_types_by_name['SitelinkPlaceholderFieldEnum'] = _SITELINKPLACEHOLDERFIELDENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SitelinkPlaceholderFieldEnum = _reflection.GeneratedProtocolMessageType('SitelinkPlaceholderFieldEnum', (_message.Message,), dict(
  DESCRIPTOR = _SITELINKPLACEHOLDERFIELDENUM,
  __module__ = 'google.ads.googleads_v1.proto.enums.sitelink_placeholder_field_pb2'
  ,
  __doc__ = """Values for Sitelink placeholder fields.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.enums.SitelinkPlaceholderFieldEnum)
  ))
_sym_db.RegisterMessage(SitelinkPlaceholderFieldEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
