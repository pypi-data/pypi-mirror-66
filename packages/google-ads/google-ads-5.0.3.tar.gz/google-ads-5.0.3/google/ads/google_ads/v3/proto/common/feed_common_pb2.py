# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/common/feed_common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/common/feed_common.proto',
  package='google.ads.googleads.v3.common',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.commonB\017FeedCommonProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/common;common\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Common\312\002\036Google\\Ads\\GoogleAds\\V3\\Common\352\002\"Google::Ads::GoogleAds::V3::Common'),
  serialized_pb=_b('\n6google/ads/googleads_v3/proto/common/feed_common.proto\x12\x1egoogle.ads.googleads.v3.common\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"p\n\x05Money\x12\x33\n\rcurrency_code\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x32\n\ramount_micros\x18\x02 \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\xea\x01\n\"com.google.ads.googleads.v3.commonB\x0f\x46\x65\x65\x64\x43ommonProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/common;common\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Common\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Common\xea\x02\"Google::Ads::GoogleAds::V3::Commonb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_MONEY = _descriptor.Descriptor(
  name='Money',
  full_name='google.ads.googleads.v3.common.Money',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='currency_code', full_name='google.ads.googleads.v3.common.Money.currency_code', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount_micros', full_name='google.ads.googleads.v3.common.Money.amount_micros', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=152,
  serialized_end=264,
)

_MONEY.fields_by_name['currency_code'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_MONEY.fields_by_name['amount_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
DESCRIPTOR.message_types_by_name['Money'] = _MONEY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Money = _reflection.GeneratedProtocolMessageType('Money', (_message.Message,), dict(
  DESCRIPTOR = _MONEY,
  __module__ = 'google.ads.googleads_v3.proto.common.feed_common_pb2'
  ,
  __doc__ = """Represents a price in a particular currency.
  
  
  Attributes:
      currency_code:
          Three-character ISO 4217 currency code.
      amount_micros:
          Amount in micros. One million is equivalent to one unit.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.common.Money)
  ))
_sym_db.RegisterMessage(Money)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
