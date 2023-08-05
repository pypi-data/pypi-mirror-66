# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/enums/content_label_type.proto

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
  name='google/ads/googleads_v1/proto/enums/content_label_type.proto',
  package='google.ads.googleads.v1.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v1.enumsB\025ContentLabelTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V1.Enums\312\002\035Google\\Ads\\GoogleAds\\V1\\Enums\352\002!Google::Ads::GoogleAds::V1::Enums'),
  serialized_pb=_b('\n<google/ads/googleads_v1/proto/enums/content_label_type.proto\x12\x1dgoogle.ads.googleads.v1.enums\x1a\x1cgoogle/api/annotations.proto\"\xed\x02\n\x14\x43ontentLabelTypeEnum\"\xd4\x02\n\x10\x43ontentLabelType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x17\n\x13SEXUALLY_SUGGESTIVE\x10\x02\x12\x12\n\x0e\x42\x45LOW_THE_FOLD\x10\x03\x12\x11\n\rPARKED_DOMAIN\x10\x04\x12\x08\n\x04GAME\x10\x05\x12\x0c\n\x08JUVENILE\x10\x06\x12\r\n\tPROFANITY\x10\x07\x12\x0b\n\x07TRAGEDY\x10\x08\x12\t\n\x05VIDEO\x10\t\x12\x15\n\x11VIDEO_RATING_DV_G\x10\n\x12\x16\n\x12VIDEO_RATING_DV_PG\x10\x0b\x12\x15\n\x11VIDEO_RATING_DV_T\x10\x0c\x12\x16\n\x12VIDEO_RATING_DV_MA\x10\r\x12\x17\n\x13VIDEO_NOT_YET_RATED\x10\x0e\x12\x12\n\x0e\x45MBEDDED_VIDEO\x10\x0f\x12\x18\n\x14LIVE_STREAMING_VIDEO\x10\x10\x42\xea\x01\n!com.google.ads.googleads.v1.enumsB\x15\x43ontentLabelTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V1.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V1\\Enums\xea\x02!Google::Ads::GoogleAds::V1::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CONTENTLABELTYPEENUM_CONTENTLABELTYPE = _descriptor.EnumDescriptor(
  name='ContentLabelType',
  full_name='google.ads.googleads.v1.enums.ContentLabelTypeEnum.ContentLabelType',
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
      name='SEXUALLY_SUGGESTIVE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BELOW_THE_FOLD', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PARKED_DOMAIN', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GAME', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JUVENILE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROFANITY', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRAGEDY', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_RATING_DV_G', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_RATING_DV_PG', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_RATING_DV_T', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_RATING_DV_MA', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VIDEO_NOT_YET_RATED', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EMBEDDED_VIDEO', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LIVE_STREAMING_VIDEO', index=16, number=16,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=151,
  serialized_end=491,
)
_sym_db.RegisterEnumDescriptor(_CONTENTLABELTYPEENUM_CONTENTLABELTYPE)


_CONTENTLABELTYPEENUM = _descriptor.Descriptor(
  name='ContentLabelTypeEnum',
  full_name='google.ads.googleads.v1.enums.ContentLabelTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONTENTLABELTYPEENUM_CONTENTLABELTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=126,
  serialized_end=491,
)

_CONTENTLABELTYPEENUM_CONTENTLABELTYPE.containing_type = _CONTENTLABELTYPEENUM
DESCRIPTOR.message_types_by_name['ContentLabelTypeEnum'] = _CONTENTLABELTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ContentLabelTypeEnum = _reflection.GeneratedProtocolMessageType('ContentLabelTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _CONTENTLABELTYPEENUM,
  __module__ = 'google.ads.googleads_v1.proto.enums.content_label_type_pb2'
  ,
  __doc__ = """Container for enum describing content label types in ContentLabel.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.enums.ContentLabelTypeEnum)
  ))
_sym_db.RegisterMessage(ContentLabelTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
