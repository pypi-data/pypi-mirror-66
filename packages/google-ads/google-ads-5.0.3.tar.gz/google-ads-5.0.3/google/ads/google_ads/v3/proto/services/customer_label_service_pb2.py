# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/services/customer_label_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v3.proto.resources import customer_label_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_customer__label__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/services/customer_label_service.proto',
  package='google.ads.googleads.v3.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v3.servicesB\031CustomerLabelServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v3/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V3.Services\312\002 Google\\Ads\\GoogleAds\\V3\\Services\352\002$Google::Ads::GoogleAds::V3::Services'),
  serialized_pb=_b('\nCgoogle/ads/googleads_v3/proto/services/customer_label_service.proto\x12 google.ads.googleads.v3.services\x1a<google/ads/googleads_v3/proto/resources/customer_label.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x17google/rpc/status.proto\"5\n\x17GetCustomerLabelRequest\x12\x1a\n\rresource_name\x18\x01 \x01(\tB\x03\xe0\x41\x02\"\xba\x01\n\x1bMutateCustomerLabelsRequest\x12\x18\n\x0b\x63ustomer_id\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12Q\n\noperations\x18\x02 \x03(\x0b\x32\x38.google.ads.googleads.v3.services.CustomerLabelOperationB\x03\xe0\x41\x02\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"{\n\x16\x43ustomerLabelOperation\x12\x42\n\x06\x63reate\x18\x01 \x01(\x0b\x32\x30.google.ads.googleads.v3.resources.CustomerLabelH\x00\x12\x10\n\x06remove\x18\x02 \x01(\tH\x00\x42\x0b\n\toperation\"\x9f\x01\n\x1cMutateCustomerLabelsResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12L\n\x07results\x18\x02 \x03(\x0b\x32;.google.ads.googleads.v3.services.MutateCustomerLabelResult\"2\n\x19MutateCustomerLabelResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xf0\x03\n\x14\x43ustomerLabelService\x12\xc9\x01\n\x10GetCustomerLabel\x12\x39.google.ads.googleads.v3.services.GetCustomerLabelRequest\x1a\x30.google.ads.googleads.v3.resources.CustomerLabel\"H\x82\xd3\xe4\x93\x02\x32\x12\x30/v3/{resource_name=customers/*/customerLabels/*}\xda\x41\rresource_name\x12\xee\x01\n\x14MutateCustomerLabels\x12=.google.ads.googleads.v3.services.MutateCustomerLabelsRequest\x1a>.google.ads.googleads.v3.services.MutateCustomerLabelsResponse\"W\x82\xd3\xe4\x93\x02\x38\"3/v3/customers/{customer_id=*}/customerLabels:mutate:\x01*\xda\x41\x16\x63ustomer_id,operations\x1a\x1b\xca\x41\x18googleads.googleapis.comB\x80\x02\n$com.google.ads.googleads.v3.servicesB\x19\x43ustomerLabelServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v3/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V3.Services\xca\x02 Google\\Ads\\GoogleAds\\V3\\Services\xea\x02$Google::Ads::GoogleAds::V3::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_customer__label__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,])




_GETCUSTOMERLABELREQUEST = _descriptor.Descriptor(
  name='GetCustomerLabelRequest',
  full_name='google.ads.googleads.v3.services.GetCustomerLabelRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.services.GetCustomerLabelRequest.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002'), file=DESCRIPTOR),
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
  serialized_start=280,
  serialized_end=333,
)


_MUTATECUSTOMERLABELSREQUEST = _descriptor.Descriptor(
  name='MutateCustomerLabelsRequest',
  full_name='google.ads.googleads.v3.services.MutateCustomerLabelsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v3.services.MutateCustomerLabelsRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v3.services.MutateCustomerLabelsRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\002'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v3.services.MutateCustomerLabelsRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v3.services.MutateCustomerLabelsRequest.validate_only', index=3,
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
  serialized_start=336,
  serialized_end=522,
)


_CUSTOMERLABELOPERATION = _descriptor.Descriptor(
  name='CustomerLabelOperation',
  full_name='google.ads.googleads.v3.services.CustomerLabelOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v3.services.CustomerLabelOperation.create', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v3.services.CustomerLabelOperation.remove', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
      name='operation', full_name='google.ads.googleads.v3.services.CustomerLabelOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=524,
  serialized_end=647,
)


_MUTATECUSTOMERLABELSRESPONSE = _descriptor.Descriptor(
  name='MutateCustomerLabelsResponse',
  full_name='google.ads.googleads.v3.services.MutateCustomerLabelsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v3.services.MutateCustomerLabelsResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v3.services.MutateCustomerLabelsResponse.results', index=1,
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
  serialized_start=650,
  serialized_end=809,
)


_MUTATECUSTOMERLABELRESULT = _descriptor.Descriptor(
  name='MutateCustomerLabelResult',
  full_name='google.ads.googleads.v3.services.MutateCustomerLabelResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.services.MutateCustomerLabelResult.resource_name', index=0,
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
  serialized_start=811,
  serialized_end=861,
)

_MUTATECUSTOMERLABELSREQUEST.fields_by_name['operations'].message_type = _CUSTOMERLABELOPERATION
_CUSTOMERLABELOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_customer__label__pb2._CUSTOMERLABEL
_CUSTOMERLABELOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMERLABELOPERATION.fields_by_name['create'])
_CUSTOMERLABELOPERATION.fields_by_name['create'].containing_oneof = _CUSTOMERLABELOPERATION.oneofs_by_name['operation']
_CUSTOMERLABELOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMERLABELOPERATION.fields_by_name['remove'])
_CUSTOMERLABELOPERATION.fields_by_name['remove'].containing_oneof = _CUSTOMERLABELOPERATION.oneofs_by_name['operation']
_MUTATECUSTOMERLABELSRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATECUSTOMERLABELSRESPONSE.fields_by_name['results'].message_type = _MUTATECUSTOMERLABELRESULT
DESCRIPTOR.message_types_by_name['GetCustomerLabelRequest'] = _GETCUSTOMERLABELREQUEST
DESCRIPTOR.message_types_by_name['MutateCustomerLabelsRequest'] = _MUTATECUSTOMERLABELSREQUEST
DESCRIPTOR.message_types_by_name['CustomerLabelOperation'] = _CUSTOMERLABELOPERATION
DESCRIPTOR.message_types_by_name['MutateCustomerLabelsResponse'] = _MUTATECUSTOMERLABELSRESPONSE
DESCRIPTOR.message_types_by_name['MutateCustomerLabelResult'] = _MUTATECUSTOMERLABELRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetCustomerLabelRequest = _reflection.GeneratedProtocolMessageType('GetCustomerLabelRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETCUSTOMERLABELREQUEST,
  __module__ = 'google.ads.googleads_v3.proto.services.customer_label_service_pb2'
  ,
  __doc__ = """Request message for
  [CustomerLabelService.GetCustomerLabel][google.ads.googleads.v3.services.CustomerLabelService.GetCustomerLabel].
  
  
  Attributes:
      resource_name:
          Required. The resource name of the customer-label relationship
          to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.GetCustomerLabelRequest)
  ))
_sym_db.RegisterMessage(GetCustomerLabelRequest)

MutateCustomerLabelsRequest = _reflection.GeneratedProtocolMessageType('MutateCustomerLabelsRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMERLABELSREQUEST,
  __module__ = 'google.ads.googleads_v3.proto.services.customer_label_service_pb2'
  ,
  __doc__ = """Request message for
  [CustomerLabelService.MutateCustomerLabels][google.ads.googleads.v3.services.CustomerLabelService.MutateCustomerLabels].
  
  
  Attributes:
      customer_id:
          Required. ID of the customer whose customer-label
          relationships are being modified.
      operations:
          Required. The list of operations to perform on customer-label
          relationships.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.MutateCustomerLabelsRequest)
  ))
_sym_db.RegisterMessage(MutateCustomerLabelsRequest)

CustomerLabelOperation = _reflection.GeneratedProtocolMessageType('CustomerLabelOperation', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERLABELOPERATION,
  __module__ = 'google.ads.googleads_v3.proto.services.customer_label_service_pb2'
  ,
  __doc__ = """A single operation (create, remove) on a customer-label relationship.
  
  
  Attributes:
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new
          customer-label relationship.
      remove:
          Remove operation: A resource name for the customer-label
          relationship being removed, in this format:
          ``customers/{customer_id}/customerLabels/{label_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.CustomerLabelOperation)
  ))
_sym_db.RegisterMessage(CustomerLabelOperation)

MutateCustomerLabelsResponse = _reflection.GeneratedProtocolMessageType('MutateCustomerLabelsResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMERLABELSRESPONSE,
  __module__ = 'google.ads.googleads_v3.proto.services.customer_label_service_pb2'
  ,
  __doc__ = """Response message for a customer labels mutate.
  
  
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
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.MutateCustomerLabelsResponse)
  ))
_sym_db.RegisterMessage(MutateCustomerLabelsResponse)

MutateCustomerLabelResult = _reflection.GeneratedProtocolMessageType('MutateCustomerLabelResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMERLABELRESULT,
  __module__ = 'google.ads.googleads_v3.proto.services.customer_label_service_pb2'
  ,
  __doc__ = """The result for a customer label mutate.
  
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.MutateCustomerLabelResult)
  ))
_sym_db.RegisterMessage(MutateCustomerLabelResult)


DESCRIPTOR._options = None
_GETCUSTOMERLABELREQUEST.fields_by_name['resource_name']._options = None
_MUTATECUSTOMERLABELSREQUEST.fields_by_name['customer_id']._options = None
_MUTATECUSTOMERLABELSREQUEST.fields_by_name['operations']._options = None

_CUSTOMERLABELSERVICE = _descriptor.ServiceDescriptor(
  name='CustomerLabelService',
  full_name='google.ads.googleads.v3.services.CustomerLabelService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=864,
  serialized_end=1360,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetCustomerLabel',
    full_name='google.ads.googleads.v3.services.CustomerLabelService.GetCustomerLabel',
    index=0,
    containing_service=None,
    input_type=_GETCUSTOMERLABELREQUEST,
    output_type=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_customer__label__pb2._CUSTOMERLABEL,
    serialized_options=_b('\202\323\344\223\0022\0220/v3/{resource_name=customers/*/customerLabels/*}\332A\rresource_name'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateCustomerLabels',
    full_name='google.ads.googleads.v3.services.CustomerLabelService.MutateCustomerLabels',
    index=1,
    containing_service=None,
    input_type=_MUTATECUSTOMERLABELSREQUEST,
    output_type=_MUTATECUSTOMERLABELSRESPONSE,
    serialized_options=_b('\202\323\344\223\0028\"3/v3/customers/{customer_id=*}/customerLabels:mutate:\001*\332A\026customer_id,operations'),
  ),
])
_sym_db.RegisterServiceDescriptor(_CUSTOMERLABELSERVICE)

DESCRIPTOR.services_by_name['CustomerLabelService'] = _CUSTOMERLABELSERVICE

# @@protoc_insertion_point(module_scope)
