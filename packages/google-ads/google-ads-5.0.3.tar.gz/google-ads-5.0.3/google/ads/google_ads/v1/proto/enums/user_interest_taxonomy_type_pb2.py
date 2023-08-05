# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/enums/user_interest_taxonomy_type.proto

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
  name='google/ads/googleads_v1/proto/enums/user_interest_taxonomy_type.proto',
  package='google.ads.googleads.v1.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v1.enumsB\035UserInterestTaxonomyTypeProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V1.Enums\312\002\035Google\\Ads\\GoogleAds\\V1\\Enums\352\002!Google::Ads::GoogleAds::V1::Enums'),
  serialized_pb=_b('\nEgoogle/ads/googleads_v1/proto/enums/user_interest_taxonomy_type.proto\x12\x1dgoogle.ads.googleads.v1.enums\x1a\x1cgoogle/api/annotations.proto\"\xbf\x01\n\x1cUserInterestTaxonomyTypeEnum\"\x9e\x01\n\x18UserInterestTaxonomyType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0c\n\x08\x41\x46\x46INITY\x10\x02\x12\r\n\tIN_MARKET\x10\x03\x12\x1b\n\x17MOBILE_APP_INSTALL_USER\x10\x04\x12\x10\n\x0cVERTICAL_GEO\x10\x05\x12\x18\n\x14NEW_SMART_PHONE_USER\x10\x06\x42\xf2\x01\n!com.google.ads.googleads.v1.enumsB\x1dUserInterestTaxonomyTypeProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V1.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V1\\Enums\xea\x02!Google::Ads::GoogleAds::V1::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_USERINTERESTTAXONOMYTYPEENUM_USERINTERESTTAXONOMYTYPE = _descriptor.EnumDescriptor(
  name='UserInterestTaxonomyType',
  full_name='google.ads.googleads.v1.enums.UserInterestTaxonomyTypeEnum.UserInterestTaxonomyType',
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
      name='AFFINITY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='IN_MARKET', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOBILE_APP_INSTALL_USER', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VERTICAL_GEO', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NEW_SMART_PHONE_USER', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=168,
  serialized_end=326,
)
_sym_db.RegisterEnumDescriptor(_USERINTERESTTAXONOMYTYPEENUM_USERINTERESTTAXONOMYTYPE)


_USERINTERESTTAXONOMYTYPEENUM = _descriptor.Descriptor(
  name='UserInterestTaxonomyTypeEnum',
  full_name='google.ads.googleads.v1.enums.UserInterestTaxonomyTypeEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _USERINTERESTTAXONOMYTYPEENUM_USERINTERESTTAXONOMYTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=135,
  serialized_end=326,
)

_USERINTERESTTAXONOMYTYPEENUM_USERINTERESTTAXONOMYTYPE.containing_type = _USERINTERESTTAXONOMYTYPEENUM
DESCRIPTOR.message_types_by_name['UserInterestTaxonomyTypeEnum'] = _USERINTERESTTAXONOMYTYPEENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserInterestTaxonomyTypeEnum = _reflection.GeneratedProtocolMessageType('UserInterestTaxonomyTypeEnum', (_message.Message,), dict(
  DESCRIPTOR = _USERINTERESTTAXONOMYTYPEENUM,
  __module__ = 'google.ads.googleads_v1.proto.enums.user_interest_taxonomy_type_pb2'
  ,
  __doc__ = """Message describing a UserInterestTaxonomyType.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.enums.UserInterestTaxonomyTypeEnum)
  ))
_sym_db.RegisterMessage(UserInterestTaxonomyTypeEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
