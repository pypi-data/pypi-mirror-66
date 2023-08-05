# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/enums/campaign_status.proto

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
  name='google/ads/googleads_v3/proto/enums/campaign_status.proto',
  package='google.ads.googleads.v3.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v3.enumsB\023CampaignStatusProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V3.Enums\312\002\035Google\\Ads\\GoogleAds\\V3\\Enums\352\002!Google::Ads::GoogleAds::V3::Enums'),
  serialized_pb=_b('\n9google/ads/googleads_v3/proto/enums/campaign_status.proto\x12\x1dgoogle.ads.googleads.v3.enums\x1a\x1cgoogle/api/annotations.proto\"j\n\x12\x43\x61mpaignStatusEnum\"T\n\x0e\x43\x61mpaignStatus\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07\x45NABLED\x10\x02\x12\n\n\x06PAUSED\x10\x03\x12\x0b\n\x07REMOVED\x10\x04\x42\xe8\x01\n!com.google.ads.googleads.v3.enumsB\x13\x43\x61mpaignStatusProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v3/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V3.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V3\\Enums\xea\x02!Google::Ads::GoogleAds::V3::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CAMPAIGNSTATUSENUM_CAMPAIGNSTATUS = _descriptor.EnumDescriptor(
  name='CampaignStatus',
  full_name='google.ads.googleads.v3.enums.CampaignStatusEnum.CampaignStatus',
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
      name='PAUSED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVED', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=144,
  serialized_end=228,
)
_sym_db.RegisterEnumDescriptor(_CAMPAIGNSTATUSENUM_CAMPAIGNSTATUS)


_CAMPAIGNSTATUSENUM = _descriptor.Descriptor(
  name='CampaignStatusEnum',
  full_name='google.ads.googleads.v3.enums.CampaignStatusEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CAMPAIGNSTATUSENUM_CAMPAIGNSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=228,
)

_CAMPAIGNSTATUSENUM_CAMPAIGNSTATUS.containing_type = _CAMPAIGNSTATUSENUM
DESCRIPTOR.message_types_by_name['CampaignStatusEnum'] = _CAMPAIGNSTATUSENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CampaignStatusEnum = _reflection.GeneratedProtocolMessageType('CampaignStatusEnum', (_message.Message,), dict(
  DESCRIPTOR = _CAMPAIGNSTATUSENUM,
  __module__ = 'google.ads.googleads_v3.proto.enums.campaign_status_pb2'
  ,
  __doc__ = """Container for enum describing possible statuses of a campaign.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.enums.CampaignStatusEnum)
  ))
_sym_db.RegisterMessage(CampaignStatusEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
