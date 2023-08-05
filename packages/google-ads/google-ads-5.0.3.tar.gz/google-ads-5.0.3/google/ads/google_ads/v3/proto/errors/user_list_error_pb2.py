# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/errors/user_list_error.proto

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
  name='google/ads/googleads_v3/proto/errors/user_list_error.proto',
  package='google.ads.googleads.v3.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.errorsB\022UserListErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Errors\312\002\036Google\\Ads\\GoogleAds\\V3\\Errors\352\002\"Google::Ads::GoogleAds::V3::Errors'),
  serialized_pb=_b('\n:google/ads/googleads_v3/proto/errors/user_list_error.proto\x12\x1egoogle.ads.googleads.v3.errors\x1a\x1cgoogle/api/annotations.proto\"\xec\x07\n\x11UserListErrorEnum\"\xd6\x07\n\rUserListError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x37\n3EXTERNAL_REMARKETING_USER_LIST_MUTATE_NOT_SUPPORTED\x10\x02\x12\x1a\n\x16\x43ONCRETE_TYPE_REQUIRED\x10\x03\x12\x1f\n\x1b\x43ONVERSION_TYPE_ID_REQUIRED\x10\x04\x12\x1e\n\x1a\x44UPLICATE_CONVERSION_TYPES\x10\x05\x12\x1b\n\x17INVALID_CONVERSION_TYPE\x10\x06\x12\x17\n\x13INVALID_DESCRIPTION\x10\x07\x12\x10\n\x0cINVALID_NAME\x10\x08\x12\x10\n\x0cINVALID_TYPE\x10\t\x12\x34\n0CAN_NOT_ADD_LOGICAL_LIST_AS_LOGICAL_LIST_OPERAND\x10\n\x12*\n&INVALID_USER_LIST_LOGICAL_RULE_OPERAND\x10\x0b\x12\x15\n\x11NAME_ALREADY_USED\x10\x0c\x12%\n!NEW_CONVERSION_TYPE_NAME_REQUIRED\x10\r\x12%\n!CONVERSION_TYPE_NAME_ALREADY_USED\x10\x0e\x12\x1e\n\x1aOWNERSHIP_REQUIRED_FOR_SET\x10\x0f\x12\"\n\x1eUSER_LIST_MUTATE_NOT_SUPPORTED\x10\x10\x12\x10\n\x0cINVALID_RULE\x10\x11\x12\x16\n\x12INVALID_DATE_RANGE\x10\x1b\x12%\n!CAN_NOT_MUTATE_SENSITIVE_USERLIST\x10\x1c\x12\x1f\n\x1bMAX_NUM_RULEBASED_USERLISTS\x10\x1d\x12\'\n#CANNOT_MODIFY_BILLABLE_RECORD_COUNT\x10\x1e\x12\x12\n\x0e\x41PP_ID_NOT_SET\x10\x1f\x12-\n)USERLIST_NAME_IS_RESERVED_FOR_SYSTEM_LIST\x10 \x12\x36\n2ADVERTISER_NOT_WHITELISTED_FOR_USING_UPLOADED_DATA\x10!\x12\x1e\n\x1aRULE_TYPE_IS_NOT_SUPPORTED\x10\"\x12:\n6CAN_NOT_ADD_A_SIMILAR_USERLIST_AS_LOGICAL_LIST_OPERAND\x10#\x12:\n6CAN_NOT_MIX_CRM_BASED_IN_LOGICAL_LIST_WITH_OTHER_LISTS\x10$B\xed\x01\n\"com.google.ads.googleads.v3.errorsB\x12UserListErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Errors\xea\x02\"Google::Ads::GoogleAds::V3::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_USERLISTERRORENUM_USERLISTERROR = _descriptor.EnumDescriptor(
  name='UserListError',
  full_name='google.ads.googleads.v3.errors.UserListErrorEnum.UserListError',
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
      name='EXTERNAL_REMARKETING_USER_LIST_MUTATE_NOT_SUPPORTED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONCRETE_TYPE_REQUIRED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONVERSION_TYPE_ID_REQUIRED', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DUPLICATE_CONVERSION_TYPES', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_CONVERSION_TYPE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_DESCRIPTION', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_NAME', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_TYPE', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAN_NOT_ADD_LOGICAL_LIST_AS_LOGICAL_LIST_OPERAND', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_USER_LIST_LOGICAL_RULE_OPERAND', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NAME_ALREADY_USED', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEW_CONVERSION_TYPE_NAME_REQUIRED', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONVERSION_TYPE_NAME_ALREADY_USED', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OWNERSHIP_REQUIRED_FOR_SET', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USER_LIST_MUTATE_NOT_SUPPORTED', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_RULE', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_DATE_RANGE', index=18, number=27,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAN_NOT_MUTATE_SENSITIVE_USERLIST', index=19, number=28,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MAX_NUM_RULEBASED_USERLISTS', index=20, number=29,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_MODIFY_BILLABLE_RECORD_COUNT', index=21, number=30,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='APP_ID_NOT_SET', index=22, number=31,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USERLIST_NAME_IS_RESERVED_FOR_SYSTEM_LIST', index=23, number=32,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADVERTISER_NOT_WHITELISTED_FOR_USING_UPLOADED_DATA', index=24, number=33,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RULE_TYPE_IS_NOT_SUPPORTED', index=25, number=34,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAN_NOT_ADD_A_SIMILAR_USERLIST_AS_LOGICAL_LIST_OPERAND', index=26, number=35,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAN_NOT_MIX_CRM_BASED_IN_LOGICAL_LIST_WITH_OTHER_LISTS', index=27, number=36,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=147,
  serialized_end=1129,
)
_sym_db.RegisterEnumDescriptor(_USERLISTERRORENUM_USERLISTERROR)


_USERLISTERRORENUM = _descriptor.Descriptor(
  name='UserListErrorEnum',
  full_name='google.ads.googleads.v3.errors.UserListErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _USERLISTERRORENUM_USERLISTERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=125,
  serialized_end=1129,
)

_USERLISTERRORENUM_USERLISTERROR.containing_type = _USERLISTERRORENUM
DESCRIPTOR.message_types_by_name['UserListErrorEnum'] = _USERLISTERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserListErrorEnum = _reflection.GeneratedProtocolMessageType('UserListErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _USERLISTERRORENUM,
  __module__ = 'google.ads.googleads_v3.proto.errors.user_list_error_pb2'
  ,
  __doc__ = """Container for enum describing possible user list errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.errors.UserListErrorEnum)
  ))
_sym_db.RegisterMessage(UserListErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
