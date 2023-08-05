# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/enums/hotel_price_bucket.proto

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
  name='google/ads/googleads_v2/proto/enums/hotel_price_bucket.proto',
  package='google.ads.googleads.v2.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v2.enumsB\025HotelPriceBucketProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V2.Enums\312\002\035Google\\Ads\\GoogleAds\\V2\\Enums\352\002!Google::Ads::GoogleAds::V2::Enums'),
  serialized_pb=_b('\n<google/ads/googleads_v2/proto/enums/hotel_price_bucket.proto\x12\x1dgoogle.ads.googleads.v2.enums\x1a\x1cgoogle/api/annotations.proto\"i\n\x14HotelPriceBucketEnum\"Q\n\x10HotelPriceBucket\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x0f\n\x0bLOWEST_TIED\x10\x03\x12\x0e\n\nNOT_LOWEST\x10\x04\x42\xea\x01\n!com.google.ads.googleads.v2.enumsB\x15HotelPriceBucketProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v2/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V2.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V2\\Enums\xea\x02!Google::Ads::GoogleAds::V2::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_HOTELPRICEBUCKETENUM_HOTELPRICEBUCKET = _descriptor.EnumDescriptor(
  name='HotelPriceBucket',
  full_name='google.ads.googleads.v2.enums.HotelPriceBucketEnum.HotelPriceBucket',
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
      name='LOWEST_TIED', index=2, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOT_LOWEST', index=3, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=149,
  serialized_end=230,
)
_sym_db.RegisterEnumDescriptor(_HOTELPRICEBUCKETENUM_HOTELPRICEBUCKET)


_HOTELPRICEBUCKETENUM = _descriptor.Descriptor(
  name='HotelPriceBucketEnum',
  full_name='google.ads.googleads.v2.enums.HotelPriceBucketEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HOTELPRICEBUCKETENUM_HOTELPRICEBUCKET,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=125,
  serialized_end=230,
)

_HOTELPRICEBUCKETENUM_HOTELPRICEBUCKET.containing_type = _HOTELPRICEBUCKETENUM
DESCRIPTOR.message_types_by_name['HotelPriceBucketEnum'] = _HOTELPRICEBUCKETENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HotelPriceBucketEnum = _reflection.GeneratedProtocolMessageType('HotelPriceBucketEnum', (_message.Message,), dict(
  DESCRIPTOR = _HOTELPRICEBUCKETENUM,
  __module__ = 'google.ads.googleads_v2.proto.enums.hotel_price_bucket_pb2'
  ,
  __doc__ = """Container for enum describing hotel price bucket for a hotel itinerary.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.enums.HotelPriceBucketEnum)
  ))
_sym_db.RegisterMessage(HotelPriceBucketEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
