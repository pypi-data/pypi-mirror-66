# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/user_list_rule_type.proto

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
  name='google/ads/googleads_v2/proto/enums/user_list_rule_type.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB\025UserListRuleTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\n=google/ads/googleads_v2/proto/enums/user_list_rule_type.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"h\n\x14UserListRuleTypeEnum\"P\n\x10UserListRuleType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0e\n\nAND_OF_ORS\x10\x02\x12\x0e\n\nOR_OF_ANDS\x10\x03\x42\xea\x01\n!com.google.ads.googleads.v2.enumsB\x15UserListRuleTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_USERLISTRULETYPEENUM_USERLISTRULETYPE = _descriptor.EnumDescriptor(
  name='UserListRuleType',
  full_name='google.ads.googleads.v2.enums.UserListRuleTypeEnum.UserListRuleType',
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
      name='AND_OF_ORS', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OR_OF_ANDS', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=150,
  serialized_end=230,
)
_sym_db.RegisterEnumDescriptor(_USERLISTRULETYPEENUM_USERLISTRULETYPE)


_USERLISTRULETYPEENUM = _descriptor.Descriptor(
  name='UserListRuleTypeEnum',
  full_name='google.ads.googleads.v2.enums.UserListRuleTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _USERLISTRULETYPEENUM_USERLISTRULETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=126,
  serialized_end=230,
)

_USERLISTRULETYPEENUM_USERLISTRULETYPE.containing_type = _USERLISTRULETYPEENUM
DESCRIPTOR.message_types_by_name['UserListRuleTypeEnum'] = _USERLISTRULETYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserListRuleTypeEnum = _reflection.GeneratedProtocolMessageType('UserListRuleTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _USERLISTRULETYPEENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.user_list_rule_type_pb2'
  ,
  __doc__ = """Rule based user list rule type.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.UserListRuleTypeEnum)
  ))
_sym_db.RegisterMessage(UserListRuleTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
