# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/resources/geo_target_constant.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v2.proto.enums import geo_target_constant_status_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_geo__target__constant__status__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v2/proto/resources/geo_target_constant.proto',
  package='google.ads.googleads.v2.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v2.resourcesB\026GeoTargetConstantProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v2/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V2.Resources\312\002!Google\\Ads\\GoogleAds\\V2\\Resources\352\002%Google::Ads::GoogleAds::V2::Resources'),
  serialized_pb=_b('\nAgoogle/ads/googleads_v2/proto/resources/geo_target_constant.proto\x12!google.ads.googleads.v2.resources\x1a\x44google/ads/googleads_v2/proto/enums/geo_target_constant_status.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\x80\x03\n\x11GeoTargetConstant\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12\'\n\x02id\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12*\n\x04name\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x32\n\x0c\x63ountry_code\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x31\n\x0btarget_type\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x62\n\x06status\x18\x07 \x01(\x0e\x32R.google.ads.googleads.v2.enums.GeoTargetConstantStatusEnum.GeoTargetConstantStatus\x12\x34\n\x0e\x63\x61nonical_name\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x83\x02\n%com.google.ads.googleads.v2.resourcesB\x16GeoTargetConstantProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v2/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V2.Resources\xca\x02!Google\\Ads\\GoogleAds\\V2\\Resources\xea\x02%Google::Ads::GoogleAds::V2::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_geo__target__constant__status__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_GEOTARGETCONSTANT = _descriptor.Descriptor(
  name='GeoTargetConstant',
  full_name='google.ads.googleads.v2.resources.GeoTargetConstant',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.resources.GeoTargetConstant.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v2.resources.GeoTargetConstant.id', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.ads.googleads.v2.resources.GeoTargetConstant.name', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='country_code', full_name='google.ads.googleads.v2.resources.GeoTargetConstant.country_code', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target_type', full_name='google.ads.googleads.v2.resources.GeoTargetConstant.target_type', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.ads.googleads.v2.resources.GeoTargetConstant.status', index=5,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='canonical_name', full_name='google.ads.googleads.v2.resources.GeoTargetConstant.canonical_name', index=6,
      number=8, type=11, cpp_type=10, label=1,
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
  serialized_start=237,
  serialized_end=621,
)

_GEOTARGETCONSTANT.fields_by_name['id'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_GEOTARGETCONSTANT.fields_by_name['name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GEOTARGETCONSTANT.fields_by_name['country_code'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GEOTARGETCONSTANT.fields_by_name['target_type'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_GEOTARGETCONSTANT.fields_by_name['status'].enum_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_geo__target__constant__status__pb2._GEOTARGETCONSTANTSTATUSENUM_GEOTARGETCONSTANTSTATUS
_GEOTARGETCONSTANT.fields_by_name['canonical_name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['GeoTargetConstant'] = _GEOTARGETCONSTANT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GeoTargetConstant = _reflection.GeneratedProtocolMessageType('GeoTargetConstant', (_message.Message,), dict(
  DESCRIPTOR = _GEOTARGETCONSTANT,
  __module__ = 'google.ads.googleads_v2.proto.resources.geo_target_constant_pb2'
  ,
  __doc__ = """A geo target constant.
  
  
  Attributes:
      resource_name:
          The resource name of the geo target constant. Geo target
          constant resource names have the form:
          ``geoTargetConstants/{geo_target_constant_id}``
      id:
          The ID of the geo target constant.
      name:
          Geo target constant English name.
      country_code:
          The ISO-3166-1 alpha-2 country code that is associated with
          the target.
      target_type:
          Geo target constant target type.
      status:
          Geo target constant status.
      canonical_name:
          The fully qualified English name, consisting of the target's
          name and that of its parent and country.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.resources.GeoTargetConstant)
  ))
_sym_db.RegisterMessage(GeoTargetConstant)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
