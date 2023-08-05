# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/errors/customer_manager_link_error.proto

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
  name='google/ads/googleads_v3/proto/errors/customer_manager_link_error.proto',
  package='google.ads.googleads.v3.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.errorsB\035CustomerManagerLinkErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Errors\312\002\036Google\\Ads\\GoogleAds\\V3\\Errors\352\002\"Google::Ads::GoogleAds::V3::Errors'),
  serialized_pb=_b('\nFgoogle/ads/googleads_v3/proto/errors/customer_manager_link_error.proto\x12\x1egoogle.ads.googleads.v3.errors\x1a\x1cgoogle/api/annotations.proto\"\xd0\x03\n\x1c\x43ustomerManagerLinkErrorEnum\"\xaf\x03\n\x18\x43ustomerManagerLinkError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x15\n\x11NO_PENDING_INVITE\x10\x02\x12\'\n#SAME_CLIENT_MORE_THAN_ONCE_PER_CALL\x10\x03\x12-\n)MANAGER_HAS_MAX_NUMBER_OF_LINKED_ACCOUNTS\x10\x04\x12-\n)CANNOT_UNLINK_ACCOUNT_WITHOUT_ACTIVE_USER\x10\x05\x12+\n\'CANNOT_REMOVE_LAST_CLIENT_ACCOUNT_OWNER\x10\x06\x12+\n\'CANNOT_CHANGE_ROLE_BY_NON_ACCOUNT_OWNER\x10\x07\x12\x32\n.CANNOT_CHANGE_ROLE_FOR_NON_ACTIVE_LINK_ACCOUNT\x10\x08\x12\x19\n\x15\x44UPLICATE_CHILD_FOUND\x10\t\x12.\n*TEST_ACCOUNT_LINKS_TOO_MANY_CHILD_ACCOUNTS\x10\nB\xf8\x01\n\"com.google.ads.googleads.v3.errorsB\x1d\x43ustomerManagerLinkErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Errors\xea\x02\"Google::Ads::GoogleAds::V3::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CUSTOMERMANAGERLINKERRORENUM_CUSTOMERMANAGERLINKERROR = _descriptor.EnumDescriptor(
  name='CustomerManagerLinkError',
  full_name='google.ads.googleads.v3.errors.CustomerManagerLinkErrorEnum.CustomerManagerLinkError',
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
      name='NO_PENDING_INVITE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SAME_CLIENT_MORE_THAN_ONCE_PER_CALL', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MANAGER_HAS_MAX_NUMBER_OF_LINKED_ACCOUNTS', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_UNLINK_ACCOUNT_WITHOUT_ACTIVE_USER', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_REMOVE_LAST_CLIENT_ACCOUNT_OWNER', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_CHANGE_ROLE_BY_NON_ACCOUNT_OWNER', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CANNOT_CHANGE_ROLE_FOR_NON_ACTIVE_LINK_ACCOUNT', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DUPLICATE_CHILD_FOUND', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TEST_ACCOUNT_LINKS_TOO_MANY_CHILD_ACCOUNTS', index=10, number=10,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=170,
  serialized_end=601,
)
_sym_db.RegisterEnumDescriptor(_CUSTOMERMANAGERLINKERRORENUM_CUSTOMERMANAGERLINKERROR)


_CUSTOMERMANAGERLINKERRORENUM = _descriptor.Descriptor(
  name='CustomerManagerLinkErrorEnum',
  full_name='google.ads.googleads.v3.errors.CustomerManagerLinkErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CUSTOMERMANAGERLINKERRORENUM_CUSTOMERMANAGERLINKERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=137,
  serialized_end=601,
)

_CUSTOMERMANAGERLINKERRORENUM_CUSTOMERMANAGERLINKERROR.containing_type = _CUSTOMERMANAGERLINKERRORENUM
DESCRIPTOR.message_types_by_name['CustomerManagerLinkErrorEnum'] = _CUSTOMERMANAGERLINKERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CustomerManagerLinkErrorEnum = _reflection.GeneratedProtocolMessageType('CustomerManagerLinkErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERMANAGERLINKERRORENUM,
  __module__ = 'google.ads.googleads_v3.proto.errors.customer_manager_link_error_pb2'
  ,
  __doc__ = """Container for enum describing possible CustomerManagerLink errors.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.errors.CustomerManagerLinkErrorEnum)
  ))
_sym_db.RegisterMessage(CustomerManagerLinkErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
