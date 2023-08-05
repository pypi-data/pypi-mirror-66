# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/resources/ad_group.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v3.proto.common import custom_parameter_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_custom__parameter__pb2
from google.ads.google_ads.v3.proto.common import explorer_auto_optimizer_setting_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_explorer__auto__optimizer__setting__pb2
from google.ads.google_ads.v3.proto.common import targeting_setting_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_targeting__setting__pb2
from google.ads.google_ads.v3.proto.enums import ad_group_ad_rotation_mode_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__ad__rotation__mode__pb2
from google.ads.google_ads.v3.proto.enums import ad_group_status_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__status__pb2
from google.ads.google_ads.v3.proto.enums import ad_group_type_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__type__pb2
from google.ads.google_ads.v3.proto.enums import bidding_source_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_bidding__source__pb2
from google.ads.google_ads.v3.proto.enums import targeting_dimension_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_targeting__dimension__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/resources/ad_group.proto',
  package='google.ads.googleads.v3.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v3.resourcesB\014AdGroupProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V3.Resources\312\002!Google\\Ads\\GoogleAds\\V3\\Resources\352\002%Google::Ads::GoogleAds::V3::Resources'),
  serialized_pb=_b('\n6google/ads/googleads_v3/proto/resources/ad_group.proto\x12!google.ads.googleads.v3.resources\x1a;google/ads/googleads_v3/proto/common/custom_parameter.proto\x1aJgoogle/ads/googleads_v3/proto/common/explorer_auto_optimizer_setting.proto\x1a<google/ads/googleads_v3/proto/common/targeting_setting.proto\x1a\x43google/ads/googleads_v3/proto/enums/ad_group_ad_rotation_mode.proto\x1a\x39google/ads/googleads_v3/proto/enums/ad_group_status.proto\x1a\x37google/ads/googleads_v3/proto/enums/ad_group_type.proto\x1a\x38google/ads/googleads_v3/proto/enums/bidding_source.proto\x1a=google/ads/googleads_v3/proto/enums/targeting_dimension.proto\x1a\x19google/api/resource.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\x8f\x0e\n\x07\x41\x64Group\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12\'\n\x02id\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12*\n\x04name\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12N\n\x06status\x18\x05 \x01(\x0e\x32>.google.ads.googleads.v3.enums.AdGroupStatusEnum.AdGroupStatus\x12H\n\x04type\x18\x0c \x01(\x0e\x32:.google.ads.googleads.v3.enums.AdGroupTypeEnum.AdGroupType\x12h\n\x10\x61\x64_rotation_mode\x18\x16 \x01(\x0e\x32N.google.ads.googleads.v3.enums.AdGroupAdRotationModeEnum.AdGroupAdRotationMode\x12\x33\n\rbase_ad_group\x18\x12 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12;\n\x15tracking_url_template\x18\r \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12N\n\x15url_custom_parameters\x18\x06 \x03(\x0b\x32/.google.ads.googleads.v3.common.CustomParameter\x12.\n\x08\x63\x61mpaign\x18\n \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x33\n\x0e\x63pc_bid_micros\x18\x0e \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x33\n\x0e\x63pm_bid_micros\x18\x0f \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x36\n\x11target_cpa_micros\x18\x1b \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x33\n\x0e\x63pv_bid_micros\x18\x11 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x36\n\x11target_cpm_micros\x18\x1a \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x31\n\x0btarget_roas\x18\x1e \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12;\n\x16percent_cpc_bid_micros\x18\x14 \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x65\n\x1f\x65xplorer_auto_optimizer_setting\x18\x15 \x01(\x0b\x32<.google.ads.googleads.v3.common.ExplorerAutoOptimizerSetting\x12n\n\x1c\x64isplay_custom_bid_dimension\x18\x17 \x01(\x0e\x32H.google.ads.googleads.v3.enums.TargetingDimensionEnum.TargetingDimension\x12\x36\n\x10\x66inal_url_suffix\x18\x18 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12K\n\x11targeting_setting\x18\x19 \x01(\x0b\x32\x30.google.ads.googleads.v3.common.TargetingSetting\x12@\n\x1b\x65\x66\x66\x65\x63tive_target_cpa_micros\x18\x1c \x01(\x0b\x32\x1b.google.protobuf.Int64Value\x12\x63\n\x1b\x65\x66\x66\x65\x63tive_target_cpa_source\x18\x1d \x01(\x0e\x32>.google.ads.googleads.v3.enums.BiddingSourceEnum.BiddingSource\x12;\n\x15\x65\x66\x66\x65\x63tive_target_roas\x18\x1f \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x64\n\x1c\x65\x66\x66\x65\x63tive_target_roas_source\x18  \x01(\x0e\x32>.google.ads.googleads.v3.enums.BiddingSourceEnum.BiddingSource\x12,\n\x06labels\x18! \x03(\x0b\x32\x1c.google.protobuf.StringValue:O\xea\x41L\n googleads.googleapis.com/AdGroup\x12(customers/{customer}/adGroups/{ad_group}B\xf9\x01\n%com.google.ads.googleads.v3.resourcesB\x0c\x41\x64GroupProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v3/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V3.Resources\xca\x02!Google\\Ads\\GoogleAds\\V3\\Resources\xea\x02%Google::Ads::GoogleAds::V3::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_custom__parameter__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_explorer__auto__optimizer__setting__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_targeting__setting__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__ad__rotation__mode__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__type__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_bidding__source__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_targeting__dimension__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_ADGROUP = _descriptor.Descriptor(
  name='AdGroup',
  full_name='google.ads.googleads.v3.resources.AdGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.resources.AdGroup.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v3.resources.AdGroup.id', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='google.ads.googleads.v3.resources.AdGroup.name', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.ads.googleads.v3.resources.AdGroup.status', index=3,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='google.ads.googleads.v3.resources.AdGroup.type', index=4,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_rotation_mode', full_name='google.ads.googleads.v3.resources.AdGroup.ad_rotation_mode', index=5,
      number=22, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='base_ad_group', full_name='google.ads.googleads.v3.resources.AdGroup.base_ad_group', index=6,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tracking_url_template', full_name='google.ads.googleads.v3.resources.AdGroup.tracking_url_template', index=7,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='url_custom_parameters', full_name='google.ads.googleads.v3.resources.AdGroup.url_custom_parameters', index=8,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='campaign', full_name='google.ads.googleads.v3.resources.AdGroup.campaign', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cpc_bid_micros', full_name='google.ads.googleads.v3.resources.AdGroup.cpc_bid_micros', index=10,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cpm_bid_micros', full_name='google.ads.googleads.v3.resources.AdGroup.cpm_bid_micros', index=11,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target_cpa_micros', full_name='google.ads.googleads.v3.resources.AdGroup.target_cpa_micros', index=12,
      number=27, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cpv_bid_micros', full_name='google.ads.googleads.v3.resources.AdGroup.cpv_bid_micros', index=13,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target_cpm_micros', full_name='google.ads.googleads.v3.resources.AdGroup.target_cpm_micros', index=14,
      number=26, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target_roas', full_name='google.ads.googleads.v3.resources.AdGroup.target_roas', index=15,
      number=30, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='percent_cpc_bid_micros', full_name='google.ads.googleads.v3.resources.AdGroup.percent_cpc_bid_micros', index=16,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='explorer_auto_optimizer_setting', full_name='google.ads.googleads.v3.resources.AdGroup.explorer_auto_optimizer_setting', index=17,
      number=21, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='display_custom_bid_dimension', full_name='google.ads.googleads.v3.resources.AdGroup.display_custom_bid_dimension', index=18,
      number=23, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='final_url_suffix', full_name='google.ads.googleads.v3.resources.AdGroup.final_url_suffix', index=19,
      number=24, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='targeting_setting', full_name='google.ads.googleads.v3.resources.AdGroup.targeting_setting', index=20,
      number=25, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='effective_target_cpa_micros', full_name='google.ads.googleads.v3.resources.AdGroup.effective_target_cpa_micros', index=21,
      number=28, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='effective_target_cpa_source', full_name='google.ads.googleads.v3.resources.AdGroup.effective_target_cpa_source', index=22,
      number=29, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='effective_target_roas', full_name='google.ads.googleads.v3.resources.AdGroup.effective_target_roas', index=23,
      number=31, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='effective_target_roas_source', full_name='google.ads.googleads.v3.resources.AdGroup.effective_target_roas_source', index=24,
      number=32, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='labels', full_name='google.ads.googleads.v3.resources.AdGroup.labels', index=25,
      number=33, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('\352AL\n googleads.googleapis.com/AdGroup\022(customers/{customer}/adGroups/{ad_group}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=688,
  serialized_end=2495,
)

_ADGROUP.fields_by_name['id'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADGROUP.fields_by_name['name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_ADGROUP.fields_by_name['status'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__status__pb2._ADGROUPSTATUSENUM_ADGROUPSTATUS
_ADGROUP.fields_by_name['type'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__type__pb2._ADGROUPTYPEENUM_ADGROUPTYPE
_ADGROUP.fields_by_name['ad_rotation_mode'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_ad__group__ad__rotation__mode__pb2._ADGROUPADROTATIONMODEENUM_ADGROUPADROTATIONMODE
_ADGROUP.fields_by_name['base_ad_group'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_ADGROUP.fields_by_name['tracking_url_template'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_ADGROUP.fields_by_name['url_custom_parameters'].message_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_custom__parameter__pb2._CUSTOMPARAMETER
_ADGROUP.fields_by_name['campaign'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_ADGROUP.fields_by_name['cpc_bid_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADGROUP.fields_by_name['cpm_bid_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADGROUP.fields_by_name['target_cpa_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADGROUP.fields_by_name['cpv_bid_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADGROUP.fields_by_name['target_cpm_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADGROUP.fields_by_name['target_roas'].message_type = google_dot_protobuf_dot_wrappers__pb2._DOUBLEVALUE
_ADGROUP.fields_by_name['percent_cpc_bid_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADGROUP.fields_by_name['explorer_auto_optimizer_setting'].message_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_explorer__auto__optimizer__setting__pb2._EXPLORERAUTOOPTIMIZERSETTING
_ADGROUP.fields_by_name['display_custom_bid_dimension'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_targeting__dimension__pb2._TARGETINGDIMENSIONENUM_TARGETINGDIMENSION
_ADGROUP.fields_by_name['final_url_suffix'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_ADGROUP.fields_by_name['targeting_setting'].message_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_common_dot_targeting__setting__pb2._TARGETINGSETTING
_ADGROUP.fields_by_name['effective_target_cpa_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_ADGROUP.fields_by_name['effective_target_cpa_source'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_bidding__source__pb2._BIDDINGSOURCEENUM_BIDDINGSOURCE
_ADGROUP.fields_by_name['effective_target_roas'].message_type = google_dot_protobuf_dot_wrappers__pb2._DOUBLEVALUE
_ADGROUP.fields_by_name['effective_target_roas_source'].enum_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_enums_dot_bidding__source__pb2._BIDDINGSOURCEENUM_BIDDINGSOURCE
_ADGROUP.fields_by_name['labels'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['AdGroup'] = _ADGROUP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdGroup = _reflection.GeneratedProtocolMessageType('AdGroup', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUP,
  __module__ = 'google.ads.googleads_v3.proto.resources.ad_group_pb2'
  ,
  __doc__ = """An ad group.
  
  
  Attributes:
      resource_name:
          The resource name of the ad group. Ad group resource names
          have the form:
          ``customers/{customer_id}/adGroups/{ad_group_id}``
      id:
          The ID of the ad group.
      name:
          The name of the ad group.  This field is required and should
          not be empty when creating new ad groups.  It must contain
          fewer than 255 UTF-8 full-width characters.  It must not
          contain any null (code point 0x0), NL line feed (code point
          0xA) or carriage return (code point 0xD) characters.
      status:
          The status of the ad group.
      type:
          The type of the ad group.
      ad_rotation_mode:
          The ad rotation mode of the ad group.
      base_ad_group:
          For draft or experiment ad groups, this field is the resource
          name of the base ad group from which this ad group was
          created. If a draft or experiment ad group does not have a
          base ad group, then this field is null.  For base ad groups,
          this field equals the ad group resource name.  This field is
          read-only.
      tracking_url_template:
          The URL template for constructing a tracking URL.
      url_custom_parameters:
          The list of mappings used to substitute custom parameter tags
          in a ``tracking_url_template``, ``final_urls``, or
          ``mobile_final_urls``.
      campaign:
          The campaign to which the ad group belongs.
      cpc_bid_micros:
          The maximum CPC (cost-per-click) bid.
      cpm_bid_micros:
          The maximum CPM (cost-per-thousand viewable impressions) bid.
      target_cpa_micros:
          The target CPA (cost-per-acquisition).
      cpv_bid_micros:
          The CPV (cost-per-view) bid.
      target_cpm_micros:
          Average amount in micros that the advertiser is willing to pay
          for every thousand times the ad is shown.
      target_roas:
          The target ROAS (return-on-ad-spend) override. If the ad
          group's campaign bidding strategy is a standard Target ROAS
          strategy, then this field overrides the target ROAS specified
          in the campaign's bidding strategy. Otherwise, this value is
          ignored.
      percent_cpc_bid_micros:
          The percent cpc bid amount, expressed as a fraction of the
          advertised price for some good or service. The valid range for
          the fraction is [0,1) and the value stored here is 1,000,000
          \* [fraction].
      explorer_auto_optimizer_setting:
          Settings for the Display Campaign Optimizer, initially termed
          "Explorer".
      display_custom_bid_dimension:
          Allows advertisers to specify a targeting dimension on which
          to place absolute bids. This is only applicable for campaigns
          that target only the display network and not search.
      final_url_suffix:
          URL template for appending params to Final URL.
      targeting_setting:
          Setting for targeting related features.
      effective_target_cpa_micros:
          The effective target CPA (cost-per-acquisition). This field is
          read-only.
      effective_target_cpa_source:
          Source of the effective target CPA. This field is read-only.
      effective_target_roas:
          The effective target ROAS (return-on-ad-spend). This field is
          read-only.
      effective_target_roas_source:
          Source of the effective target ROAS. This field is read-only.
      labels:
          The resource names of labels attached to this ad group.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.resources.AdGroup)
  ))
_sym_db.RegisterMessage(AdGroup)


DESCRIPTOR._options = None
_ADGROUP._options = None
# @@protoc_insertion_point(module_scope)
