# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/call_placeholder_field.proto

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
  name='google/ads/googleads_v2/proto/enums/call_placeholder_field.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB\031CallPlaceholderFieldProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\n@google/ads/googleads_v2/proto/enums/call_placeholder_field.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"\xba\x01\n\x18\x43\x61llPlaceholderFieldEnum\"\x9d\x01\n\x14\x43\x61llPlaceholderField\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x10\n\x0cPHONE_NUMBER\x10\x02\x12\x10\n\x0c\x43OUNTRY_CODE\x10\x03\x12\x0b\n\x07TRACKED\x10\x04\x12\x16\n\x12\x43ONVERSION_TYPE_ID\x10\x05\x12\x1e\n\x1a\x43ONVERSION_REPORTING_STATE\x10\x06\x42\xee\x01\n!com.google.ads.googleads.v2.enumsB\x19\x43\x61llPlaceholderFieldProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CALLPLACEHOLDERFIELDENUM_CALLPLACEHOLDERFIELD = _descriptor.EnumDescriptor(
  name='CallPlaceholderField',
  full_name='google.ads.googleads.v2.enums.CallPlaceholderFieldEnum.CallPlaceholderField',
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
      name='PHONE_NUMBER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COUNTRY_CODE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRACKED', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONVERSION_TYPE_ID', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONVERSION_REPORTING_STATE', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=159,
  serialized_end=316,
)
_sym_db.RegisterEnumDescriptor(_CALLPLACEHOLDERFIELDENUM_CALLPLACEHOLDERFIELD)


_CALLPLACEHOLDERFIELDENUM = _descriptor.Descriptor(
  name='CallPlaceholderFieldEnum',
  full_name='google.ads.googleads.v2.enums.CallPlaceholderFieldEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CALLPLACEHOLDERFIELDENUM_CALLPLACEHOLDERFIELD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=130,
  serialized_end=316,
)

_CALLPLACEHOLDERFIELDENUM_CALLPLACEHOLDERFIELD.containing_type = _CALLPLACEHOLDERFIELDENUM
DESCRIPTOR.message_types_by_name['CallPlaceholderFieldEnum'] = _CALLPLACEHOLDERFIELDENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CallPlaceholderFieldEnum = _reflection.GeneratedProtocolMessageType('CallPlaceholderFieldEnum', (_message.Message,), dict(
  DESCRIPTOR = _CALLPLACEHOLDERFIELDENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.call_placeholder_field_pb2'
  ,
  __doc__ = """Values for Call placeholder fields.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.CallPlaceholderFieldEnum)
  ))
_sym_db.RegisterMessage(CallPlaceholderFieldEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
