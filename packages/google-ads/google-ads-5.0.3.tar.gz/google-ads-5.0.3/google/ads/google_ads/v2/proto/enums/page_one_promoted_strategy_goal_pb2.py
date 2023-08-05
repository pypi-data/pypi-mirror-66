# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/page_one_promoted_strategy_goal.proto

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
  name='google/ads/googleads_v2/proto/enums/page_one_promoted_strategy_goal.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB PageOnePromotedStrategyGoalProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\nIgoogle/ads/googleads_v2/proto/enums/page_one_promoted_strategy_goal.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"\x87\x01\n\x1fPageOnePromotedStrategyGoalEnum\"d\n\x1bPageOnePromotedStrategyGoal\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0e\n\nFIRST_PAGE\x10\x02\x12\x17\n\x13\x46IRST_PAGE_PROMOTED\x10\x03\x42\xf5\x01\n!com.google.ads.googleads.v2.enumsB PageOnePromotedStrategyGoalProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_PAGEONEPROMOTEDSTRATEGYGOALENUM_PAGEONEPROMOTEDSTRATEGYGOAL = _descriptor.EnumDescriptor(
  name='PageOnePromotedStrategyGoal',
  full_name='google.ads.googleads.v2.enums.PageOnePromotedStrategyGoalEnum.PageOnePromotedStrategyGoal',
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
      name='FIRST_PAGE', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FIRST_PAGE_PROMOTED', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=174,
  serialized_end=274,
)
_sym_db.RegisterEnumDescriptor(_PAGEONEPROMOTEDSTRATEGYGOALENUM_PAGEONEPROMOTEDSTRATEGYGOAL)


_PAGEONEPROMOTEDSTRATEGYGOALENUM = _descriptor.Descriptor(
  name='PageOnePromotedStrategyGoalEnum',
  full_name='google.ads.googleads.v2.enums.PageOnePromotedStrategyGoalEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PAGEONEPROMOTEDSTRATEGYGOALENUM_PAGEONEPROMOTEDSTRATEGYGOAL,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=139,
  serialized_end=274,
)

_PAGEONEPROMOTEDSTRATEGYGOALENUM_PAGEONEPROMOTEDSTRATEGYGOAL.containing_type = _PAGEONEPROMOTEDSTRATEGYGOALENUM
DESCRIPTOR.message_types_by_name['PageOnePromotedStrategyGoalEnum'] = _PAGEONEPROMOTEDSTRATEGYGOALENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PageOnePromotedStrategyGoalEnum = _reflection.GeneratedProtocolMessageType('PageOnePromotedStrategyGoalEnum', (_message.Message,), dict(
  DESCRIPTOR = _PAGEONEPROMOTEDSTRATEGYGOALENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.page_one_promoted_strategy_goal_pb2'
  ,
  __doc__ = """Container for enum describing possible strategy goals: where impressions
  are desired to be shown on search result pages.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.PageOnePromotedStrategyGoalEnum)
  ))
_sym_db.RegisterMessage(PageOnePromotedStrategyGoalEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
