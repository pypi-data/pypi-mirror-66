# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/enums/budget_status.proto

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
  name='google/ads/googleads_v1/proto/enums/budget_status.proto',
  package='google.ads.googleads.v1.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v1.enumsB\021BudgetStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V1.Enums\312\002\035Google\\Ads\\GoogleAds\\V1\\Enums\352\002!Google::Ads::GoogleAds::V1::Enums'),
  serialized_pb=_b('\n7google/ads/googleads_v1/proto/enums/budget_status.proto\x12\x1dgoogle.ads.googleads.v1.enums\x1a\x1cgoogle/api/annotations.proto\"Z\n\x10\x42udgetStatusEnum\"F\n\x0c\x42udgetStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07\x45NABLED\x10\x02\x12\x0b\n\x07REMOVED\x10\x03\x42\xe6\x01\n!com.google.ads.googleads.v1.enumsB\x11\x42udgetStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V1.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V1\\Enums\xea\x02!Google::Ads::GoogleAds::V1::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_BUDGETSTATUSENUM_BUDGETSTATUS = _descriptor.EnumDescriptor(
  name='BudgetStatus',
  full_name='google.ads.googleads.v1.enums.BudgetStatusEnum.BudgetStatus',
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
      name='ENABLED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVED', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=140,
  serialized_end=210,
)
_sym_db.RegisterEnumDescriptor(_BUDGETSTATUSENUM_BUDGETSTATUS)


_BUDGETSTATUSENUM = _descriptor.Descriptor(
  name='BudgetStatusEnum',
  full_name='google.ads.googleads.v1.enums.BudgetStatusEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BUDGETSTATUSENUM_BUDGETSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=210,
)

_BUDGETSTATUSENUM_BUDGETSTATUS.containing_type = _BUDGETSTATUSENUM
DESCRIPTOR.message_types_by_name['BudgetStatusEnum'] = _BUDGETSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BudgetStatusEnum = _reflection.GeneratedProtocolMessageType('BudgetStatusEnum', (_message.Message,), dict(
  DESCRIPTOR = _BUDGETSTATUSENUM,
  __module__ = 'google.ads.googleads_v1.proto.enums.budget_status_pb2'
  ,
  __doc__ = """Message describing a Budget status
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.enums.BudgetStatusEnum)
  ))
_sym_db.RegisterMessage(BudgetStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
