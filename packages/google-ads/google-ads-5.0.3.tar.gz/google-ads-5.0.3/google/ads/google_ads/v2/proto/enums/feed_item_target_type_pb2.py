# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/feed_item_target_type.proto

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
  name='google/ads/googleads_v2/proto/enums/feed_item_target_type.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB\027FeedItemTargetTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\n?google/ads/googleads_v2/proto/enums/feed_item_target_type.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"w\n\x16\x46\x65\x65\x64ItemTargetTypeEnum\"]\n\x12\x46\x65\x65\x64ItemTargetType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0c\n\x08\x43\x41MPAIGN\x10\x02\x12\x0c\n\x08\x41\x44_GROUP\x10\x03\x12\r\n\tCRITERION\x10\x04\x42\xec\x01\n!com.google.ads.googleads.v2.enumsB\x17\x46\x65\x65\x64ItemTargetTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_FEEDITEMTARGETTYPEENUM_FEEDITEMTARGETTYPE = _descriptor.EnumDescriptor(
  name='FeedItemTargetType',
  full_name='google.ads.googleads.v2.enums.FeedItemTargetTypeEnum.FeedItemTargetType',
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
      name='CAMPAIGN', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AD_GROUP', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRITERION', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=154,
  serialized_end=247,
)
_sym_db.RegisterEnumDescriptor(_FEEDITEMTARGETTYPEENUM_FEEDITEMTARGETTYPE)


_FEEDITEMTARGETTYPEENUM = _descriptor.Descriptor(
  name='FeedItemTargetTypeEnum',
  full_name='google.ads.googleads.v2.enums.FeedItemTargetTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FEEDITEMTARGETTYPEENUM_FEEDITEMTARGETTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=247,
)

_FEEDITEMTARGETTYPEENUM_FEEDITEMTARGETTYPE.containing_type = _FEEDITEMTARGETTYPEENUM
DESCRIPTOR.message_types_by_name['FeedItemTargetTypeEnum'] = _FEEDITEMTARGETTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FeedItemTargetTypeEnum = _reflection.GeneratedProtocolMessageType('FeedItemTargetTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _FEEDITEMTARGETTYPEENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.feed_item_target_type_pb2'
  ,
  __doc__ = """Container for enum describing possible types of a feed item target.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.FeedItemTargetTypeEnum)
  ))
_sym_db.RegisterMessage(FeedItemTargetTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
