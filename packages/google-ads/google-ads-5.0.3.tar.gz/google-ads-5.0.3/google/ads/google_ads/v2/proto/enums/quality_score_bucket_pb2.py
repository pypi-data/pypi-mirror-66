# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/quality_score_bucket.proto

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
  name='google/ads/googleads_v2/proto/enums/quality_score_bucket.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB\027QualityScoreBucketProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\n>google/ads/googleads_v2/proto/enums/quality_score_bucket.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"\x7f\n\x16QualityScoreBucketEnum\"e\n\x12QualityScoreBucket\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x11\n\rBELOW_AVERAGE\x10\x02\x12\x0b\n\x07\x41VERAGE\x10\x03\x12\x11\n\rABOVE_AVERAGE\x10\x04\x42\xec\x01\n!com.google.ads.googleads.v2.enumsB\x17QualityScoreBucketProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_QUALITYSCOREBUCKETENUM_QUALITYSCOREBUCKET = _descriptor.EnumDescriptor(
  name='QualityScoreBucket',
  full_name='google.ads.googleads.v2.enums.QualityScoreBucketEnum.QualityScoreBucket',
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
      name='BELOW_AVERAGE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AVERAGE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ABOVE_AVERAGE', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=153,
  serialized_end=254,
)
_sym_db.RegisterEnumDescriptor(_QUALITYSCOREBUCKETENUM_QUALITYSCOREBUCKET)


_QUALITYSCOREBUCKETENUM = _descriptor.Descriptor(
  name='QualityScoreBucketEnum',
  full_name='google.ads.googleads.v2.enums.QualityScoreBucketEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _QUALITYSCOREBUCKETENUM_QUALITYSCOREBUCKET,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=127,
  serialized_end=254,
)

_QUALITYSCOREBUCKETENUM_QUALITYSCOREBUCKET.containing_type = _QUALITYSCOREBUCKETENUM
DESCRIPTOR.message_types_by_name['QualityScoreBucketEnum'] = _QUALITYSCOREBUCKETENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

QualityScoreBucketEnum = _reflection.GeneratedProtocolMessageType('QualityScoreBucketEnum', (_message.Message,), dict(
  DESCRIPTOR = _QUALITYSCOREBUCKETENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.quality_score_bucket_pb2'
  ,
  __doc__ = """The relative performance compared to other advertisers.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.QualityScoreBucketEnum)
  ))
_sym_db.RegisterMessage(QualityScoreBucketEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
