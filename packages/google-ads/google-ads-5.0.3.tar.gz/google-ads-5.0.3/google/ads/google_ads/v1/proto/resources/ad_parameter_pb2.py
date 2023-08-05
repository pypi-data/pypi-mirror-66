# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/resources/ad_parameter.proto

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
  name='google/ads/googleads_v1/proto/resources/ad_parameter.proto',
  package='google.ads.googleads.v1.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v1.resourcesB\020AdParameterProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v1/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V1.Resources\312\002!Google\\Ads\\GoogleAds\\V1\\Resources\352\002%Google::Ads::GoogleAds::V1::Resources'),
  serialized_pb=_b('\n:google/ads/googleads_v1/proto/resources/ad_parameter.proto\x12!google.ads.googleads.v1.resources\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\xca\x01\n\x0b\x41\x64Parameter\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12\x38\n\x12\x61\x64_group_criterion\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x34\n\x0fparameter_index\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x34\n\x0einsertion_text\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\xfd\x01\n%com.google.ads.googleads.v1.resourcesB\x10\x41\x64ParameterProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v1/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V1.Resources\xca\x02!Google\\Ads\\GoogleAds\\V1\\Resources\xea\x02%Google::Ads::GoogleAds::V1::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_ADPARAMETER = _descriptor.Descriptor(
  name='AdParameter',
  full_name='google.ads.googleads.v1.resources.AdParameter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.resources.AdParameter.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_group_criterion', full_name='google.ads.googleads.v1.resources.AdParameter.ad_group_criterion', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameter_index', full_name='google.ads.googleads.v1.resources.AdParameter.parameter_index', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='insertion_text', full_name='google.ads.googleads.v1.resources.AdParameter.insertion_text', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=160,
  serialized_end=362,
)

_ADPARAMETER.fields_by_name['ad_group_criterion'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_ADPARAMETER.fields_by_name['parameter_index'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADPARAMETER.fields_by_name['insertion_text'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['AdParameter'] = _ADPARAMETER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdParameter = _reflection.GeneratedProtocolMessageType('AdParameter', (_message.Message,), dict(
  DESCRIPTOR = _ADPARAMETER,
  __module__ = 'google.ads.googleads_v1.proto.resources.ad_parameter_pb2'
  ,
  __doc__ = """An ad parameter that is used to update numeric values (such as prices or
  inventory levels) in any text line of an ad (including URLs). There can
  be a maximum of two AdParameters per ad group criterion. (One with
  parameter\_index = 1 and one with parameter\_index = 2.) In the ad the
  parameters are referenced by a placeholder of the form "{param#:value}".
  E.g. "{param1:$17}"
  
  
  Attributes:
      resource_name:
          The resource name of the ad parameter. Ad parameter resource
          names have the form:  ``customers/{customer_id}/adParameters/{
          ad_group_id}~{criterion_id}~{parameter_index}``
      ad_group_criterion:
          The ad group criterion that this ad parameter belongs to.
      parameter_index:
          The unique index of this ad parameter. Must be either 1 or 2.
      insertion_text:
          Numeric value to insert into the ad text. The following
          restrictions apply: - Can use comma or period as a separator,
          with an optional period or comma (respectively) for fractional
          values. For example, 1,000,000.00 and 2.000.000,10 are valid.
          - Can be prepended or appended with a currency symbol. For
          example, $99.99 is valid. - Can be prepended or appended with
          a currency code. For example, 99.99USD and EUR200 are valid. -
          Can use '%'. For example, 1.0% and 1,0% are valid. - Can use
          plus or minus. For example, -10.99 and 25+ are valid. - Can
          use '/' between two numbers. For example 4/1 and 0.95/0.45 are
          valid.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.resources.AdParameter)
  ))
_sym_db.RegisterMessage(AdParameter)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
