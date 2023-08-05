# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/resources/ad_group_ad.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v2.proto.common import policy_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_common_dot_policy__pb2
from google.ads.google_ads.v2.proto.enums import ad_group_ad_status_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_ad__group__ad__status__pb2
from google.ads.google_ads.v2.proto.enums import ad_strength_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_ad__strength__pb2
from google.ads.google_ads.v2.proto.enums import policy_approval_status_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_policy__approval__status__pb2
from google.ads.google_ads.v2.proto.enums import policy_review_status_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_policy__review__status__pb2
from google.ads.google_ads.v2.proto.resources import ad_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_ad__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v2/proto/resources/ad_group_ad.proto',
  package='google.ads.googleads.v2.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v2.resourcesB\016AdGroupAdProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v2/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V2.Resources\312\002!Google\\Ads\\GoogleAds\\V2\\Resources\352\002%Google::Ads::GoogleAds::V2::Resources'),
  serialized_pb=_b('\n9google/ads/googleads_v2/proto/resources/ad_group_ad.proto\x12!google.ads.googleads.v2.resources\x1a\x31google/ads/googleads_v2/proto/common/policy.proto\x1a<google/ads/googleads_v2/proto/enums/ad_group_ad_status.proto\x1a\x35google/ads/googleads_v2/proto/enums/ad_strength.proto\x1a@google/ads/googleads_v2/proto/enums/policy_approval_status.proto\x1a>google/ads/googleads_v2/proto/enums/policy_review_status.proto\x1a\x30google/ads/googleads_v2/proto/resources/ad.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\xfb\x02\n\tAdGroupAd\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12R\n\x06status\x18\x03 \x01(\x0e\x32\x42.google.ads.googleads.v2.enums.AdGroupAdStatusEnum.AdGroupAdStatus\x12.\n\x08\x61\x64_group\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12\x31\n\x02\x61\x64\x18\x05 \x01(\x0b\x32%.google.ads.googleads.v2.resources.Ad\x12Q\n\x0epolicy_summary\x18\x06 \x01(\x0b\x32\x39.google.ads.googleads.v2.resources.AdGroupAdPolicySummary\x12M\n\x0b\x61\x64_strength\x18\x07 \x01(\x0e\x32\x38.google.ads.googleads.v2.enums.AdStrengthEnum.AdStrength\"\xb0\x02\n\x16\x41\x64GroupAdPolicySummary\x12N\n\x14policy_topic_entries\x18\x01 \x03(\x0b\x32\x30.google.ads.googleads.v2.common.PolicyTopicEntry\x12_\n\rreview_status\x18\x02 \x01(\x0e\x32H.google.ads.googleads.v2.enums.PolicyReviewStatusEnum.PolicyReviewStatus\x12\x65\n\x0f\x61pproval_status\x18\x03 \x01(\x0e\x32L.google.ads.googleads.v2.enums.PolicyApprovalStatusEnum.PolicyApprovalStatusB\xfb\x01\n%com.google.ads.googleads.v2.resourcesB\x0e\x41\x64GroupAdProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v2/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V2.Resources\xca\x02!Google\\Ads\\GoogleAds\\V2\\Resources\xea\x02%Google::Ads::GoogleAds::V2::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v2_dot_proto_dot_common_dot_policy__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_ad__group__ad__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_ad__strength__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_policy__approval__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_policy__review__status__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_ad__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_ADGROUPAD = _descriptor.Descriptor(
  name='AdGroupAd',
  full_name='google.ads.googleads.v2.resources.AdGroupAd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.resources.AdGroupAd.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='google.ads.googleads.v2.resources.AdGroupAd.status', index=1,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_group', full_name='google.ads.googleads.v2.resources.AdGroupAd.ad_group', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad', full_name='google.ads.googleads.v2.resources.AdGroupAd.ad', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='policy_summary', full_name='google.ads.googleads.v2.resources.AdGroupAd.policy_summary', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ad_strength', full_name='google.ads.googleads.v2.resources.AdGroupAd.ad_strength', index=5,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=507,
  serialized_end=886,
)


_ADGROUPADPOLICYSUMMARY = _descriptor.Descriptor(
  name='AdGroupAdPolicySummary',
  full_name='google.ads.googleads.v2.resources.AdGroupAdPolicySummary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='policy_topic_entries', full_name='google.ads.googleads.v2.resources.AdGroupAdPolicySummary.policy_topic_entries', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='review_status', full_name='google.ads.googleads.v2.resources.AdGroupAdPolicySummary.review_status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='approval_status', full_name='google.ads.googleads.v2.resources.AdGroupAdPolicySummary.approval_status', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=889,
  serialized_end=1193,
)

_ADGROUPAD.fields_by_name['status'].enum_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_ad__group__ad__status__pb2._ADGROUPADSTATUSENUM_ADGROUPADSTATUS
_ADGROUPAD.fields_by_name['ad_group'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_ADGROUPAD.fields_by_name['ad'].message_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_ad__pb2._AD
_ADGROUPAD.fields_by_name['policy_summary'].message_type = _ADGROUPADPOLICYSUMMARY
_ADGROUPAD.fields_by_name['ad_strength'].enum_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_ad__strength__pb2._ADSTRENGTHENUM_ADSTRENGTH
_ADGROUPADPOLICYSUMMARY.fields_by_name['policy_topic_entries'].message_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_common_dot_policy__pb2._POLICYTOPICENTRY
_ADGROUPADPOLICYSUMMARY.fields_by_name['review_status'].enum_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_policy__review__status__pb2._POLICYREVIEWSTATUSENUM_POLICYREVIEWSTATUS
_ADGROUPADPOLICYSUMMARY.fields_by_name['approval_status'].enum_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_enums_dot_policy__approval__status__pb2._POLICYAPPROVALSTATUSENUM_POLICYAPPROVALSTATUS
DESCRIPTOR.message_types_by_name['AdGroupAd'] = _ADGROUPAD
DESCRIPTOR.message_types_by_name['AdGroupAdPolicySummary'] = _ADGROUPADPOLICYSUMMARY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AdGroupAd = _reflection.GeneratedProtocolMessageType('AdGroupAd', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPAD,
  __module__ = 'google.ads.googleads_v2.proto.resources.ad_group_ad_pb2'
  ,
  __doc__ = """An ad group ad.
  
  
  Attributes:
      resource_name:
          The resource name of the ad. Ad group ad resource names have
          the form:
          ``customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}``
      status:
          The status of the ad.
      ad_group:
          The ad group to which the ad belongs.
      ad:
          The ad.
      policy_summary:
          Policy information for the ad.
      ad_strength:
          Overall ad strength for this ad group ad.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.resources.AdGroupAd)
  ))
_sym_db.RegisterMessage(AdGroupAd)

AdGroupAdPolicySummary = _reflection.GeneratedProtocolMessageType('AdGroupAdPolicySummary', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPADPOLICYSUMMARY,
  __module__ = 'google.ads.googleads_v2.proto.resources.ad_group_ad_pb2'
  ,
  __doc__ = """Contains policy information for an ad.
  
  
  Attributes:
      policy_topic_entries:
          The list of policy findings for this ad.
      review_status:
          Where in the review process this ad is.
      approval_status:
          The overall approval status of this ad, calculated based on
          the status of its individual policy topic entries.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.resources.AdGroupAdPolicySummary)
  ))
_sym_db.RegisterMessage(AdGroupAdPolicySummary)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
