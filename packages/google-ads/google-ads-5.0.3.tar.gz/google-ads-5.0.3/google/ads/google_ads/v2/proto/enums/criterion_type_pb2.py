# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/criterion_type.proto

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
  name='google/ads/googleads_v2/proto/enums/criterion_type.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB\022CriterionTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\n8google/ads/googleads_v2/proto/enums/criterion_type.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"\xd4\x04\n\x11\x43riterionTypeEnum\"\xbe\x04\n\rCriterionType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0b\n\x07KEYWORD\x10\x02\x12\r\n\tPLACEMENT\x10\x03\x12\x17\n\x13MOBILE_APP_CATEGORY\x10\x04\x12\x16\n\x12MOBILE_APPLICATION\x10\x05\x12\n\n\x06\x44\x45VICE\x10\x06\x12\x0c\n\x08LOCATION\x10\x07\x12\x11\n\rLISTING_GROUP\x10\x08\x12\x0f\n\x0b\x41\x44_SCHEDULE\x10\t\x12\r\n\tAGE_RANGE\x10\n\x12\n\n\x06GENDER\x10\x0b\x12\x10\n\x0cINCOME_RANGE\x10\x0c\x12\x13\n\x0fPARENTAL_STATUS\x10\r\x12\x11\n\rYOUTUBE_VIDEO\x10\x0e\x12\x13\n\x0fYOUTUBE_CHANNEL\x10\x0f\x12\r\n\tUSER_LIST\x10\x10\x12\r\n\tPROXIMITY\x10\x11\x12\t\n\x05TOPIC\x10\x12\x12\x11\n\rLISTING_SCOPE\x10\x13\x12\x0c\n\x08LANGUAGE\x10\x14\x12\x0c\n\x08IP_BLOCK\x10\x15\x12\x11\n\rCONTENT_LABEL\x10\x16\x12\x0b\n\x07\x43\x41RRIER\x10\x17\x12\x11\n\rUSER_INTEREST\x10\x18\x12\x0b\n\x07WEBPAGE\x10\x19\x12\x1c\n\x18OPERATING_SYSTEM_VERSION\x10\x1a\x12\x15\n\x11\x41PP_PAYMENT_MODEL\x10\x1b\x12\x11\n\rMOBILE_DEVICE\x10\x1c\x12\x13\n\x0f\x43USTOM_AFFINITY\x10\x1d\x12\x11\n\rCUSTOM_INTENT\x10\x1e\x12\x12\n\x0eLOCATION_GROUP\x10\x1f\x42\xe7\x01\n!com.google.ads.googleads.v2.enumsB\x12\x43riterionTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CRITERIONTYPEENUM_CRITERIONTYPE = _descriptor.EnumDescriptor(
  name='CriterionType',
  full_name='google.ads.googleads.v2.enums.CriterionTypeEnum.CriterionType',
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
      name='KEYWORD', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PLACEMENT', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOBILE_APP_CATEGORY', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOBILE_APPLICATION', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOCATION', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LISTING_GROUP', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AD_SCHEDULE', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AGE_RANGE', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GENDER', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INCOME_RANGE', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PARENTAL_STATUS', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YOUTUBE_VIDEO', index=14, number=14,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YOUTUBE_CHANNEL', index=15, number=15,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USER_LIST', index=16, number=16,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROXIMITY', index=17, number=17,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TOPIC', index=18, number=18,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LISTING_SCOPE', index=19, number=19,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LANGUAGE', index=20, number=20,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IP_BLOCK', index=21, number=21,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONTENT_LABEL', index=22, number=22,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CARRIER', index=23, number=23,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USER_INTEREST', index=24, number=24,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WEBPAGE', index=25, number=25,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OPERATING_SYSTEM_VERSION', index=26, number=26,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='APP_PAYMENT_MODEL', index=27, number=27,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOBILE_DEVICE', index=28, number=28,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM_AFFINITY', index=29, number=29,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CUSTOM_INTENT', index=30, number=30,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOCATION_GROUP', index=31, number=31,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=144,
  serialized_end=718,
)
_sym_db.RegisterEnumDescriptor(_CRITERIONTYPEENUM_CRITERIONTYPE)


_CRITERIONTYPEENUM = _descriptor.Descriptor(
  name='CriterionTypeEnum',
  full_name='google.ads.googleads.v2.enums.CriterionTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CRITERIONTYPEENUM_CRITERIONTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=718,
)

_CRITERIONTYPEENUM_CRITERIONTYPE.containing_type = _CRITERIONTYPEENUM
DESCRIPTOR.message_types_by_name['CriterionTypeEnum'] = _CRITERIONTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CriterionTypeEnum = _reflection.GeneratedProtocolMessageType('CriterionTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _CRITERIONTYPEENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.criterion_type_pb2'
  ,
  __doc__ = """The possible types of a criterion.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.CriterionTypeEnum)
  ))
_sym_db.RegisterMessage(CriterionTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
