# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/enums/customer_pay_per_conversion_eligibility_failure_reason.proto

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
  name='google/ads/googleads_v1/proto/enums/customer_pay_per_conversion_eligibility_failure_reason.proto',
  package='google.ads.googleads.v1.enums',
  syntax='proto3',
  serialized_options=_b('\n!com.google.ads.googleads.v1.enumsB5CustomerPayPerConversionEligibilityFailureReasonProtoP\001ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\242\002\003GAA\252\002\035Google.Ads.GoogleAds.V1.Enums\312\002\035Google\\Ads\\GoogleAds\\V1\\Enums\352\002!Google::Ads::GoogleAds::V1::Enums'),
  serialized_pb=_b('\n`google/ads/googleads_v1/proto/enums/customer_pay_per_conversion_eligibility_failure_reason.proto\x12\x1dgoogle.ads.googleads.v1.enums\x1a\x1cgoogle/api/annotations.proto\"\xd1\x02\n4CustomerPayPerConversionEligibilityFailureReasonEnum\"\x98\x02\n0CustomerPayPerConversionEligibilityFailureReason\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0b\n\x07UNKNOWN\x10\x01\x12\x1a\n\x16NOT_ENOUGH_CONVERSIONS\x10\x02\x12\x1b\n\x17\x43ONVERSION_LAG_TOO_HIGH\x10\x03\x12#\n\x1fHAS_CAMPAIGN_WITH_SHARED_BUDGET\x10\x04\x12 \n\x1cHAS_UPLOAD_CLICKS_CONVERSION\x10\x05\x12 \n\x1c\x41VERAGE_DAILY_SPEND_TOO_HIGH\x10\x06\x12\x19\n\x15\x41NALYSIS_NOT_COMPLETE\x10\x07\x12\t\n\x05OTHER\x10\x08\x42\x8a\x02\n!com.google.ads.googleads.v1.enumsB5CustomerPayPerConversionEligibilityFailureReasonProtoP\x01ZBgoogle.golang.org/genproto/googleapis/ads/googleads/v1/enums;enums\xa2\x02\x03GAA\xaa\x02\x1dGoogle.Ads.GoogleAds.V1.Enums\xca\x02\x1dGoogle\\Ads\\GoogleAds\\V1\\Enums\xea\x02!Google::Ads::GoogleAds::V1::Enumsb\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,])



_CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASONENUM_CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASON = _descriptor.EnumDescriptor(
  name='CustomerPayPerConversionEligibilityFailureReason',
  full_name='google.ads.googleads.v1.enums.CustomerPayPerConversionEligibilityFailureReasonEnum.CustomerPayPerConversionEligibilityFailureReason',
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
      name='NOT_ENOUGH_CONVERSIONS', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONVERSION_LAG_TOO_HIGH', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HAS_CAMPAIGN_WITH_SHARED_BUDGET', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HAS_UPLOAD_CLICKS_CONVERSION', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AVERAGE_DAILY_SPEND_TOO_HIGH', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ANALYSIS_NOT_COMPLETE', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OTHER', index=8, number=8,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=219,
  serialized_end=499,
)
_sym_db.RegisterEnumDescriptor(_CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASONENUM_CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASON)


_CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASONENUM = _descriptor.Descriptor(
  name='CustomerPayPerConversionEligibilityFailureReasonEnum',
  full_name='google.ads.googleads.v1.enums.CustomerPayPerConversionEligibilityFailureReasonEnum',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASONENUM_CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASON,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=162,
  serialized_end=499,
)

_CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASONENUM_CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASON.containing_type = _CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASONENUM
DESCRIPTOR.message_types_by_name['CustomerPayPerConversionEligibilityFailureReasonEnum'] = _CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASONENUM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CustomerPayPerConversionEligibilityFailureReasonEnum = _reflection.GeneratedProtocolMessageType('CustomerPayPerConversionEligibilityFailureReasonEnum', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERPAYPERCONVERSIONELIGIBILITYFAILUREREASONENUM,
  __module__ = 'google.ads.googleads_v1.proto.enums.customer_pay_per_conversion_eligibility_failure_reason_pb2'
  ,
  __doc__ = """Container for enum describing reasons why a customer is not eligible to
  use PaymentMode.CONVERSIONS.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.enums.CustomerPayPerConversionEligibilityFailureReasonEnum)
  ))
_sym_db.RegisterMessage(CustomerPayPerConversionEligibilityFailureReasonEnum)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
