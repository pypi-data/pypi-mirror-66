# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/errors/keyword_plan_negative_keyword_error.proto

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
  name='google/ads/googleads_v3/proto/errors/keyword_plan_negative_keyword_error.proto',
  package='google.ads.googleads.v3.errors',
  syntax='proto3',
  serialized_options=_b('\n\"com.google.ads.googleads.v3.errorsB$KeywordPlanNegativeKeywordErrorProtoP\001ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\242\002\003GAA\252\002\036Google.Ads.GoogleAds.V3.Errors\312\002\036Google\\Ads\\GoogleAds\\V3\\Errors\352\002\"Google::Ads::GoogleAds::V3::Errors'),
  serialized_pb=_b('\nNgoogle/ads/googleads_v3/proto/errors/keyword_plan_negative_keyword_error.proto\x12\x1egoogle.ads.googleads.v3.errors\x1a\x1cgoogle/api/annotations.proto\"f\n#KeywordPlanNegativeKeywordErrorEnum\"?\n\x1fKeywordPlanNegativeKeywordError\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x42\xff\x01\n\"com.google.ads.googleads.v3.errorsB$KeywordPlanNegativeKeywordErrorProtoP\x01ZDgoogle.golang.org/genproto/googleapis/ads/googleads/v3/errors;errors\xa2\x02\x03GAA\xaa\x02\x1eGoogle.Ads.GoogleAds.V3.Errors\xca\x02\x1eGoogle\\Ads\\GoogleAds\\V3\\Errors\xea\x02\"Google::Ads::GoogleAds::V3::Errorsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_KEYWORDPLANNEGATIVEKEYWORDERRORENUM_KEYWORDPLANNEGATIVEKEYWORDERROR = _descriptor.EnumDescriptor(
  name='KeywordPlanNegativeKeywordError',
  full_name='google.ads.googleads.v3.errors.KeywordPlanNegativeKeywordErrorEnum.KeywordPlanNegativeKeywordError',
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
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=183,
  serialized_end=246,
)
_sym_db.RegisterEnumDescriptor(_KEYWORDPLANNEGATIVEKEYWORDERRORENUM_KEYWORDPLANNEGATIVEKEYWORDERROR)


_KEYWORDPLANNEGATIVEKEYWORDERRORENUM = _descriptor.Descriptor(
  name='KeywordPlanNegativeKeywordErrorEnum',
  full_name='google.ads.googleads.v3.errors.KeywordPlanNegativeKeywordErrorEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _KEYWORDPLANNEGATIVEKEYWORDERRORENUM_KEYWORDPLANNEGATIVEKEYWORDERROR,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=144,
  serialized_end=246,
)

_KEYWORDPLANNEGATIVEKEYWORDERRORENUM_KEYWORDPLANNEGATIVEKEYWORDERROR.containing_type = _KEYWORDPLANNEGATIVEKEYWORDERRORENUM
DESCRIPTOR.message_types_by_name['KeywordPlanNegativeKeywordErrorEnum'] = _KEYWORDPLANNEGATIVEKEYWORDERRORENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

KeywordPlanNegativeKeywordErrorEnum = _reflection.GeneratedProtocolMessageType('KeywordPlanNegativeKeywordErrorEnum', (_message.Message,), dict(
  DESCRIPTOR = _KEYWORDPLANNEGATIVEKEYWORDERRORENUM,
  __module__ = 'google.ads.googleads_v3.proto.errors.keyword_plan_negative_keyword_error_pb2'
  ,
  __doc__ = """Container for enum describing possible errors from applying a keyword
  plan negative keyword.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.errors.KeywordPlanNegativeKeywordErrorEnum)
  ))
_sym_db.RegisterMessage(KeywordPlanNegativeKeywordErrorEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
