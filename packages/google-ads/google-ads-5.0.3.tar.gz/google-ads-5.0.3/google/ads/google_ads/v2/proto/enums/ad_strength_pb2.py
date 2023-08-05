# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/ad_strength.proto

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
  name='google/ads/googleads_v2/proto/enums/ad_strength.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB\017AdStrengthProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\n5google/ads/googleads_v2/proto/enums/ad_strength.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"\x85\x01\n\x0e\x41\x64StrengthEnum\"s\n\nAdStrength\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07PENDING\x10\x02\x12\n\n\x06NO_ADS\x10\x03\x12\x08\n\x04POOR\x10\x04\x12\x0b\n\x07\x41VERAGE\x10\x05\x12\x08\n\x04GOOD\x10\x06\x12\r\n\tEXCELLENT\x10\x07\x42\xe4\x01\n!com.google.ads.googleads.v2.enumsB\x0f\x41\x64StrengthProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_ADSTRENGTHENUM_ADSTRENGTH = _descriptor.EnumDescriptor(
  name='AdStrength',
  full_name='google.ads.googleads.v2.enums.AdStrengthEnum.AdStrength',
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
      name='PENDING', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NO_ADS', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POOR', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AVERAGE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GOOD', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXCELLENT', index=7, number=7,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=137,
  serialized_end=252,
)
_sym_db.RegisterEnumDescriptor(_ADSTRENGTHENUM_ADSTRENGTH)


_ADSTRENGTHENUM = _descriptor.Descriptor(
  name='AdStrengthEnum',
  full_name='google.ads.googleads.v2.enums.AdStrengthEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ADSTRENGTHENUM_ADSTRENGTH,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=252,
)

_ADSTRENGTHENUM_ADSTRENGTH.containing_type = _ADSTRENGTHENUM
DESCRIPTOR.message_types_by_name['AdStrengthEnum'] = _ADSTRENGTHENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdStrengthEnum = _reflection.GeneratedProtocolMessageType('AdStrengthEnum', (_message.Message,), dict(
  DESCRIPTOR = _ADSTRENGTHENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.ad_strength_pb2'
  ,
  __doc__ = """Container for enum describing possible ad strengths.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.AdStrengthEnum)
  ))
_sym_db.RegisterMessage(AdStrengthEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
