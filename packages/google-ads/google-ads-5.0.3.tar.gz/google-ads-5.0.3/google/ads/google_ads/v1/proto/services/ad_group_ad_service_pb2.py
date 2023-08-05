# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v1/proto/services/ad_group_ad_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v1.proto.common import policy_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_common_dot_policy__pb2
from google.ads.google_ads.v1.proto.resources import ad_group_ad_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_ad__group__ad__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v1/proto/services/ad_group_ad_service.proto',
  package='google.ads.googleads.v1.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v1.servicesB\025AdGroupAdServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V1.Services\312\002 Google\\Ads\\GoogleAds\\V1\\Services\352\002$Google::Ads::GoogleAds::V1::Services'),
  serialized_pb=_b('\n@google/ads/googleads_v1/proto/services/ad_group_ad_service.proto\x12 google.ads.googleads.v1.services\x1a\x31google/ads/googleads_v1/proto/common/policy.proto\x1a\x39google/ads/googleads_v1/proto/resources/ad_group_ad.proto\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x17google/rpc/status.proto\",\n\x13GetAdGroupAdRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t\"\xa8\x01\n\x17MutateAdGroupAdsRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\x12H\n\noperations\x18\x02 \x03(\x0b\x32\x34.google.ads.googleads.v1.services.AdGroupAdOperation\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"\xc4\x02\n\x12\x41\x64GroupAdOperation\x12/\n\x0bupdate_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12^\n\x1bpolicy_validation_parameter\x18\x05 \x01(\x0b\x32\x39.google.ads.googleads.v1.common.PolicyValidationParameter\x12>\n\x06\x63reate\x18\x01 \x01(\x0b\x32,.google.ads.googleads.v1.resources.AdGroupAdH\x00\x12>\n\x06update\x18\x02 \x01(\x0b\x32,.google.ads.googleads.v1.resources.AdGroupAdH\x00\x12\x10\n\x06remove\x18\x03 \x01(\tH\x00\x42\x0b\n\toperation\"\x97\x01\n\x18MutateAdGroupAdsResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12H\n\x07results\x18\x02 \x03(\x0b\x32\x37.google.ads.googleads.v1.services.MutateAdGroupAdResult\".\n\x15MutateAdGroupAdResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\x86\x03\n\x10\x41\x64GroupAdService\x12\xa9\x01\n\x0cGetAdGroupAd\x12\x35.google.ads.googleads.v1.services.GetAdGroupAdRequest\x1a,.google.ads.googleads.v1.resources.AdGroupAd\"4\x82\xd3\xe4\x93\x02.\x12,/v1/{resource_name=customers/*/adGroupAds/*}\x12\xc5\x01\n\x10MutateAdGroupAds\x12\x39.google.ads.googleads.v1.services.MutateAdGroupAdsRequest\x1a:.google.ads.googleads.v1.services.MutateAdGroupAdsResponse\":\x82\xd3\xe4\x93\x02\x34\"//v1/customers/{customer_id=*}/adGroupAds:mutate:\x01*B\xfc\x01\n$com.google.ads.googleads.v1.servicesB\x15\x41\x64GroupAdServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v1/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V1.Services\xca\x02 Google\\Ads\\GoogleAds\\V1\\Services\xea\x02$Google::Ads::GoogleAds::V1::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v1_dot_proto_dot_common_dot_policy__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_ad__group__ad__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,])




_GETADGROUPADREQUEST = _descriptor.Descriptor(
  name='GetAdGroupAdRequest',
  full_name='google.ads.googleads.v1.services.GetAdGroupAdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.services.GetAdGroupAdRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=333,
  serialized_end=377,
)


_MUTATEADGROUPADSREQUEST = _descriptor.Descriptor(
  name='MutateAdGroupAdsRequest',
  full_name='google.ads.googleads.v1.services.MutateAdGroupAdsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v1.services.MutateAdGroupAdsRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v1.services.MutateAdGroupAdsRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v1.services.MutateAdGroupAdsRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v1.services.MutateAdGroupAdsRequest.validate_only', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=380,
  serialized_end=548,
)


_ADGROUPADOPERATION = _descriptor.Descriptor(
  name='AdGroupAdOperation',
  full_name='google.ads.googleads.v1.services.AdGroupAdOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='google.ads.googleads.v1.services.AdGroupAdOperation.update_mask', index=0,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='policy_validation_parameter', full_name='google.ads.googleads.v1.services.AdGroupAdOperation.policy_validation_parameter', index=1,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v1.services.AdGroupAdOperation.create', index=2,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update', full_name='google.ads.googleads.v1.services.AdGroupAdOperation.update', index=3,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v1.services.AdGroupAdOperation.remove', index=4,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
    _descriptor.OneofDescriptor(
      name='operation', full_name='google.ads.googleads.v1.services.AdGroupAdOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=551,
  serialized_end=875,
)


_MUTATEADGROUPADSRESPONSE = _descriptor.Descriptor(
  name='MutateAdGroupAdsResponse',
  full_name='google.ads.googleads.v1.services.MutateAdGroupAdsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v1.services.MutateAdGroupAdsResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v1.services.MutateAdGroupAdsResponse.results', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=878,
  serialized_end=1029,
)


_MUTATEADGROUPADRESULT = _descriptor.Descriptor(
  name='MutateAdGroupAdResult',
  full_name='google.ads.googleads.v1.services.MutateAdGroupAdResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v1.services.MutateAdGroupAdResult.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=1031,
  serialized_end=1077,
)

_MUTATEADGROUPADSREQUEST.fields_by_name['operations'].message_type = _ADGROUPADOPERATION
_ADGROUPADOPERATION.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_ADGROUPADOPERATION.fields_by_name['policy_validation_parameter'].message_type = google_dot_ads_dot_googleads__v1_dot_proto_dot_common_dot_policy__pb2._POLICYVALIDATIONPARAMETER
_ADGROUPADOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_ad__group__ad__pb2._ADGROUPAD
_ADGROUPADOPERATION.fields_by_name['update'].message_type = google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_ad__group__ad__pb2._ADGROUPAD
_ADGROUPADOPERATION.oneofs_by_name['operation'].fields.append(
  _ADGROUPADOPERATION.fields_by_name['create'])
_ADGROUPADOPERATION.fields_by_name['create'].containing_oneof = _ADGROUPADOPERATION.oneofs_by_name['operation']
_ADGROUPADOPERATION.oneofs_by_name['operation'].fields.append(
  _ADGROUPADOPERATION.fields_by_name['update'])
_ADGROUPADOPERATION.fields_by_name['update'].containing_oneof = _ADGROUPADOPERATION.oneofs_by_name['operation']
_ADGROUPADOPERATION.oneofs_by_name['operation'].fields.append(
  _ADGROUPADOPERATION.fields_by_name['remove'])
_ADGROUPADOPERATION.fields_by_name['remove'].containing_oneof = _ADGROUPADOPERATION.oneofs_by_name['operation']
_MUTATEADGROUPADSRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATEADGROUPADSRESPONSE.fields_by_name['results'].message_type = _MUTATEADGROUPADRESULT
DESCRIPTOR.message_types_by_name['GetAdGroupAdRequest'] = _GETADGROUPADREQUEST
DESCRIPTOR.message_types_by_name['MutateAdGroupAdsRequest'] = _MUTATEADGROUPADSREQUEST
DESCRIPTOR.message_types_by_name['AdGroupAdOperation'] = _ADGROUPADOPERATION
DESCRIPTOR.message_types_by_name['MutateAdGroupAdsResponse'] = _MUTATEADGROUPADSRESPONSE
DESCRIPTOR.message_types_by_name['MutateAdGroupAdResult'] = _MUTATEADGROUPADRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAdGroupAdRequest = _reflection.GeneratedProtocolMessageType('GetAdGroupAdRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETADGROUPADREQUEST,
  __module__ = 'google.ads.googleads_v1.proto.services.ad_group_ad_service_pb2'
  ,
  __doc__ = """Request message for
  [AdGroupAdService.GetAdGroupAd][google.ads.googleads.v1.services.AdGroupAdService.GetAdGroupAd].
  
  
  Attributes:
      resource_name:
          The resource name of the ad to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.GetAdGroupAdRequest)
  ))
_sym_db.RegisterMessage(GetAdGroupAdRequest)

MutateAdGroupAdsRequest = _reflection.GeneratedProtocolMessageType('MutateAdGroupAdsRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEADGROUPADSREQUEST,
  __module__ = 'google.ads.googleads_v1.proto.services.ad_group_ad_service_pb2'
  ,
  __doc__ = """Request message for
  [AdGroupAdService.MutateAdGroupAds][google.ads.googleads.v1.services.AdGroupAdService.MutateAdGroupAds].
  
  
  Attributes:
      customer_id:
          The ID of the customer whose ads are being modified.
      operations:
          The list of operations to perform on individual ads.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.MutateAdGroupAdsRequest)
  ))
_sym_db.RegisterMessage(MutateAdGroupAdsRequest)

AdGroupAdOperation = _reflection.GeneratedProtocolMessageType('AdGroupAdOperation', (_message.Message,), dict(
  DESCRIPTOR = _ADGROUPADOPERATION,
  __module__ = 'google.ads.googleads_v1.proto.services.ad_group_ad_service_pb2'
  ,
  __doc__ = """A single operation (create, update, remove) on an ad group ad.
  
  
  Attributes:
      update_mask:
          FieldMask that determines which resource fields are modified
          in an update.
      policy_validation_parameter:
          Configuration for how policies are validated.
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new ad.
      update:
          Update operation: The ad is expected to have a valid resource
          name.
      remove:
          Remove operation: A resource name for the removed ad is
          expected, in this format:
          ``customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.AdGroupAdOperation)
  ))
_sym_db.RegisterMessage(AdGroupAdOperation)

MutateAdGroupAdsResponse = _reflection.GeneratedProtocolMessageType('MutateAdGroupAdsResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEADGROUPADSRESPONSE,
  __module__ = 'google.ads.googleads_v1.proto.services.ad_group_ad_service_pb2'
  ,
  __doc__ = """Response message for an ad group ad mutate.
  
  
  Attributes:
      partial_failure_error:
          Errors that pertain to operation failures in the partial
          failure mode. Returned only when partial\_failure = true and
          all errors occur inside the operations. If any errors occur
          outside the operations (e.g. auth errors), we return an RPC
          level error.
      results:
          All results for the mutate.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.MutateAdGroupAdsResponse)
  ))
_sym_db.RegisterMessage(MutateAdGroupAdsResponse)

MutateAdGroupAdResult = _reflection.GeneratedProtocolMessageType('MutateAdGroupAdResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEADGROUPADRESULT,
  __module__ = 'google.ads.googleads_v1.proto.services.ad_group_ad_service_pb2'
  ,
  __doc__ = """The result for the ad mutate.
  
  
  Attributes:
      resource_name:
          The resource name returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v1.services.MutateAdGroupAdResult)
  ))
_sym_db.RegisterMessage(MutateAdGroupAdResult)


DESCRIPTOR._options = None

_ADGROUPADSERVICE = _descriptor.ServiceDescriptor(
  name='AdGroupAdService',
  full_name='google.ads.googleads.v1.services.AdGroupAdService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1080,
  serialized_end=1470,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAdGroupAd',
    full_name='google.ads.googleads.v1.services.AdGroupAdService.GetAdGroupAd',
    index=0,
    containing_service=None,
    input_type=_GETADGROUPADREQUEST,
    output_type=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_ad__group__ad__pb2._ADGROUPAD,
    serialized_options=_b('\202\323\344\223\002.\022,/v1/{resource_name=customers/*/adGroupAds/*}'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateAdGroupAds',
    full_name='google.ads.googleads.v1.services.AdGroupAdService.MutateAdGroupAds',
    index=1,
    containing_service=None,
    input_type=_MUTATEADGROUPADSREQUEST,
    output_type=_MUTATEADGROUPADSRESPONSE,
    serialized_options=_b('\202\323\344\223\0024\"//v1/customers/{customer_id=*}/adGroupAds:mutate:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_ADGROUPADSERVICE)

DESCRIPTOR.services_by_name['AdGroupAdService'] = _ADGROUPADSERVICE

# @@protoc_insertion_point(module_scope)
