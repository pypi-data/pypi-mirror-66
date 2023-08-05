# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/errors/date_error.proto

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
  name='google/ads/googleads_v3/proto/errors/date_error.proto',
  package='google.ads.googleads.v3.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.errorsB\016DateErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Errors\312\002\036Google\\Ads\\GoogleAds\\V3\\Errors\352\002\"Google::Ads::GoogleAds::V3::Errors'),
  serialized_pb=_b('\n5google/ads/googleads_v3/proto/errors/date_error.proto\x12\x1egoogle.ads.googleads.v3.errors\x1a\x1cgoogle/api/annotations.proto\"\xbf\x03\n\rDateErrorEnum\"\xad\x03\n\tDateError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12 \n\x1cINVALID_FIELD_VALUES_IN_DATE\x10\x02\x12%\n!INVALID_FIELD_VALUES_IN_DATE_TIME\x10\x03\x12\x17\n\x13INVALID_STRING_DATE\x10\x04\x12#\n\x1fINVALID_STRING_DATE_TIME_MICROS\x10\x06\x12$\n INVALID_STRING_DATE_TIME_SECONDS\x10\x0b\x12\x30\n,INVALID_STRING_DATE_TIME_SECONDS_WITH_OFFSET\x10\x0c\x12\x1d\n\x19\x45\x41RLIER_THAN_MINIMUM_DATE\x10\x07\x12\x1b\n\x17LATER_THAN_MAXIMUM_DATE\x10\x08\x12\x33\n/DATE_RANGE_MINIMUM_DATE_LATER_THAN_MAXIMUM_DATE\x10\t\x12\x32\n.DATE_RANGE_MINIMUM_AND_MAXIMUM_DATES_BOTH_NULL\x10\nB\xe9\x01\n\"com.google.ads.googleads.v3.errorsB\x0e\x44\x61teErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Errors\xea\x02\"Google::Ads::GoogleAds::V3::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_DATEERRORENUM_DATEERROR = _descriptor.EnumDescriptor(
  name='DateError',
  full_name='google.ads.googleads.v3.errors.DateErrorEnum.DateError',
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
      name='INVALID_FIELD_VALUES_IN_DATE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_FIELD_VALUES_IN_DATE_TIME', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_STRING_DATE', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_STRING_DATE_TIME_MICROS', index=5, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_STRING_DATE_TIME_SECONDS', index=6, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_STRING_DATE_TIME_SECONDS_WITH_OFFSET', index=7, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EARLIER_THAN_MINIMUM_DATE', index=8, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LATER_THAN_MAXIMUM_DATE', index=9, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DATE_RANGE_MINIMUM_DATE_LATER_THAN_MAXIMUM_DATE', index=10, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DATE_RANGE_MINIMUM_AND_MAXIMUM_DATES_BOTH_NULL', index=11, number=10,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=138,
  serialized_end=567,
)
_sym_db.RegisterEnumDescriptor(_DATEERRORENUM_DATEERROR)


_DATEERRORENUM = _descriptor.Descriptor(
  name='DateErrorEnum',
  full_name='google.ads.googleads.v3.errors.DateErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DATEERRORENUM_DATEERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=567,
)

_DATEERRORENUM_DATEERROR.containing_type = _DATEERRORENUM
DESCRIPTOR.message_types_by_name['DateErrorEnum'] = _DATEERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DateErrorEnum = _reflection.GeneratedProtocolMessageType('DateErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _DATEERRORENUM,
  __module__ = 'google.ads.googleads_v3.proto.errors.date_error_pb2'
  ,
  __doc__ = """Container for enum describing possible date errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.errors.DateErrorEnum)
  ))
_sym_db.RegisterMessage(DateErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
