# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/target_cpa_opt_in_recommendation_goal.proto

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
  name='google/ads/googleads_v2/proto/enums/target_cpa_opt_in_recommendation_goal.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB%TargetCpaOptInRecommendationGoalProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\nOgoogle/ads/googleads_v2/proto/enums/target_cpa_opt_in_recommendation_goal.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"\xad\x01\n$TargetCpaOptInRecommendationGoalEnum\"\x84\x01\n TargetCpaOptInRecommendationGoal\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\r\n\tSAME_COST\x10\x02\x12\x14\n\x10SAME_CONVERSIONS\x10\x03\x12\x0c\n\x08SAME_CPA\x10\x04\x12\x0f\n\x0b\x43LOSEST_CPA\x10\x05\x42\xfa\x01\n!com.google.ads.googleads.v2.enumsB%TargetCpaOptInRecommendationGoalProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_TARGETCPAOPTINRECOMMENDATIONGOALENUM_TARGETCPAOPTINRECOMMENDATIONGOAL = _descriptor.EnumDescriptor(
  name='TargetCpaOptInRecommendationGoal',
  full_name='google.ads.googleads.v2.enums.TargetCpaOptInRecommendationGoalEnum.TargetCpaOptInRecommendationGoal',
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
      name='SAME_COST', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SAME_CONVERSIONS', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SAME_CPA', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLOSEST_CPA', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=186,
  serialized_end=318,
)
_sym_db.RegisterEnumDescriptor(_TARGETCPAOPTINRECOMMENDATIONGOALENUM_TARGETCPAOPTINRECOMMENDATIONGOAL)


_TARGETCPAOPTINRECOMMENDATIONGOALENUM = _descriptor.Descriptor(
  name='TargetCpaOptInRecommendationGoalEnum',
  full_name='google.ads.googleads.v2.enums.TargetCpaOptInRecommendationGoalEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TARGETCPAOPTINRECOMMENDATIONGOALENUM_TARGETCPAOPTINRECOMMENDATIONGOAL,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=145,
  serialized_end=318,
)

_TARGETCPAOPTINRECOMMENDATIONGOALENUM_TARGETCPAOPTINRECOMMENDATIONGOAL.containing_type = _TARGETCPAOPTINRECOMMENDATIONGOALENUM
DESCRIPTOR.message_types_by_name['TargetCpaOptInRecommendationGoalEnum'] = _TARGETCPAOPTINRECOMMENDATIONGOALENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TargetCpaOptInRecommendationGoalEnum = _reflection.GeneratedProtocolMessageType('TargetCpaOptInRecommendationGoalEnum', (_message.Message,), dict(
  DESCRIPTOR = _TARGETCPAOPTINRECOMMENDATIONGOALENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.target_cpa_opt_in_recommendation_goal_pb2'
  ,
  __doc__ = """Container for enum describing goals for TargetCpaOptIn recommendation.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.TargetCpaOptInRecommendationGoalEnum)
  ))
_sym_db.RegisterMessage(TargetCpaOptInRecommendationGoalEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
