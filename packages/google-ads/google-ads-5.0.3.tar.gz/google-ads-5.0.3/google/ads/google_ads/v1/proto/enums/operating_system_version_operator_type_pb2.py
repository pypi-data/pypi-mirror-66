# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/enums/operating_system_version_operator_type.proto

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
  name='google/ads/googleads_v1/proto/enums/operating_system_version_operator_type.proto',
  package='google.ads.googleads.v1.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v1.enumsB\'OperatingSystemVersionOperatorTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V1.Enums\312\002\035Google\\Ads\\GoogleAds\\V1\\Enums\352\002!Google::Ads::GoogleAds::V1::Enums'),
  serialized_pb=_b('\nPgoogle/ads/googleads_v1/proto/enums/operating_system_version_operator_type.proto\x12\x1dgoogle.ads.googleads.v1.enums\x1a\x1cgoogle/api/annotations.proto\"\x97\x01\n&OperatingSystemVersionOperatorTypeEnum\"m\n\"OperatingSystemVersionOperatorType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\r\n\tEQUALS_TO\x10\x02\x12\x1a\n\x16GREATER_THAN_EQUALS_TO\x10\x04\x42\xfc\x01\n!com.google.ads.googleads.v1.enumsB\'OperatingSystemVersionOperatorTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V1.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V1\\Enums\xea\x02!Google::Ads::GoogleAds::V1::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_OPERATINGSYSTEMVERSIONOPERATORTYPEENUM_OPERATINGSYSTEMVERSIONOPERATORTYPE = _descriptor.EnumDescriptor(
  name='OperatingSystemVersionOperatorType',
  full_name='google.ads.googleads.v1.enums.OperatingSystemVersionOperatorTypeEnum.OperatingSystemVersionOperatorType',
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
      name='EQUALS_TO', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GREATER_THAN_EQUALS_TO', index=3, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=188,
  serialized_end=297,
)
_sym_db.RegisterEnumDescriptor(_OPERATINGSYSTEMVERSIONOPERATORTYPEENUM_OPERATINGSYSTEMVERSIONOPERATORTYPE)


_OPERATINGSYSTEMVERSIONOPERATORTYPEENUM = _descriptor.Descriptor(
  name='OperatingSystemVersionOperatorTypeEnum',
  full_name='google.ads.googleads.v1.enums.OperatingSystemVersionOperatorTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _OPERATINGSYSTEMVERSIONOPERATORTYPEENUM_OPERATINGSYSTEMVERSIONOPERATORTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=146,
  serialized_end=297,
)

_OPERATINGSYSTEMVERSIONOPERATORTYPEENUM_OPERATINGSYSTEMVERSIONOPERATORTYPE.containing_type = _OPERATINGSYSTEMVERSIONOPERATORTYPEENUM
DESCRIPTOR.message_types_by_name['OperatingSystemVersionOperatorTypeEnum'] = _OPERATINGSYSTEMVERSIONOPERATORTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OperatingSystemVersionOperatorTypeEnum = _reflection.GeneratedProtocolMessageType('OperatingSystemVersionOperatorTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _OPERATINGSYSTEMVERSIONOPERATORTYPEENUM,
  __module__ = 'google.ads.googleads_v1.proto.enums.operating_system_version_operator_type_pb2'
  ,
  __doc__ = """Container for enum describing the type of OS operators.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.enums.OperatingSystemVersionOperatorTypeEnum)
  ))
_sym_db.RegisterMessage(OperatingSystemVersionOperatorTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
