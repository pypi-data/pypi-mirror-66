# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/services/customer_extension_setting_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v2.proto.resources import customer_extension_setting_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_customer__extension__setting__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v2/proto/services/customer_extension_setting_service.proto',
  package='google.ads.googleads.v2.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v2.servicesB$CustomerExtensionSettingServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v2/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V2.Services\312\002 Google\\Ads\\GoogleAds\\V2\\Services\352\002$Google::Ads::GoogleAds::V2::Services'),
  serialized_pb=_b('\nOgoogle/ads/googleads_v2/proto/services/customer_extension_setting_service.proto\x12 google.ads.googleads.v2.services\x1aHgoogle/ads/googleads_v2/proto/resources/customer_extension_setting.proto\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a\x17google/rpc/status.proto\x1a\x17google/api/client.proto\";\n\"GetCustomerExtensionSettingRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t\"\xc6\x01\n&MutateCustomerExtensionSettingsRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\x12W\n\noperations\x18\x02 \x03(\x0b\x32\x43.google.ads.googleads.v2.services.CustomerExtensionSettingOperation\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"\x91\x02\n!CustomerExtensionSettingOperation\x12/\n\x0bupdate_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12M\n\x06\x63reate\x18\x01 \x01(\x0b\x32;.google.ads.googleads.v2.resources.CustomerExtensionSettingH\x00\x12M\n\x06update\x18\x02 \x01(\x0b\x32;.google.ads.googleads.v2.resources.CustomerExtensionSettingH\x00\x12\x10\n\x06remove\x18\x03 \x01(\tH\x00\x42\x0b\n\toperation\"\xb5\x01\n\'MutateCustomerExtensionSettingsResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12W\n\x07results\x18\x02 \x03(\x0b\x32\x46.google.ads.googleads.v2.services.MutateCustomerExtensionSettingResult\"=\n$MutateCustomerExtensionSettingResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xaa\x04\n\x1f\x43ustomerExtensionSettingService\x12\xe5\x01\n\x1bGetCustomerExtensionSetting\x12\x44.google.ads.googleads.v2.services.GetCustomerExtensionSettingRequest\x1a;.google.ads.googleads.v2.resources.CustomerExtensionSetting\"C\x82\xd3\xe4\x93\x02=\x12;/v2/{resource_name=customers/*/customerExtensionSettings/*}\x12\x81\x02\n\x1fMutateCustomerExtensionSettings\x12H.google.ads.googleads.v2.services.MutateCustomerExtensionSettingsRequest\x1aI.google.ads.googleads.v2.services.MutateCustomerExtensionSettingsResponse\"I\x82\xd3\xe4\x93\x02\x43\">/v2/customers/{customer_id=*}/customerExtensionSettings:mutate:\x01*\x1a\x1b\xca\x41\x18googleads.googleapis.comB\x8b\x02\n$com.google.ads.googleads.v2.servicesB$CustomerExtensionSettingServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v2/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V2.Services\xca\x02 Google\\Ads\\GoogleAds\\V2\\Services\xea\x02$Google::Ads::GoogleAds::V2::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_customer__extension__setting__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,])




_GETCUSTOMEREXTENSIONSETTINGREQUEST = _descriptor.Descriptor(
  name='GetCustomerExtensionSettingRequest',
  full_name='google.ads.googleads.v2.services.GetCustomerExtensionSettingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.services.GetCustomerExtensionSettingRequest.resource_name', index=0,
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
  serialized_start=305,
  serialized_end=364,
)


_MUTATECUSTOMEREXTENSIONSETTINGSREQUEST = _descriptor.Descriptor(
  name='MutateCustomerExtensionSettingsRequest',
  full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingsRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingsRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingsRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingsRequest.validate_only', index=3,
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
  serialized_start=367,
  serialized_end=565,
)


_CUSTOMEREXTENSIONSETTINGOPERATION = _descriptor.Descriptor(
  name='CustomerExtensionSettingOperation',
  full_name='google.ads.googleads.v2.services.CustomerExtensionSettingOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='google.ads.googleads.v2.services.CustomerExtensionSettingOperation.update_mask', index=0,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v2.services.CustomerExtensionSettingOperation.create', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update', full_name='google.ads.googleads.v2.services.CustomerExtensionSettingOperation.update', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v2.services.CustomerExtensionSettingOperation.remove', index=3,
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
      name='operation', full_name='google.ads.googleads.v2.services.CustomerExtensionSettingOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=568,
  serialized_end=841,
)


_MUTATECUSTOMEREXTENSIONSETTINGSRESPONSE = _descriptor.Descriptor(
  name='MutateCustomerExtensionSettingsResponse',
  full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingsResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingsResponse.results', index=1,
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
  serialized_start=844,
  serialized_end=1025,
)


_MUTATECUSTOMEREXTENSIONSETTINGRESULT = _descriptor.Descriptor(
  name='MutateCustomerExtensionSettingResult',
  full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.services.MutateCustomerExtensionSettingResult.resource_name', index=0,
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
  serialized_start=1027,
  serialized_end=1088,
)

_MUTATECUSTOMEREXTENSIONSETTINGSREQUEST.fields_by_name['operations'].message_type = _CUSTOMEREXTENSIONSETTINGOPERATION
_CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_customer__extension__setting__pb2._CUSTOMEREXTENSIONSETTING
_CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['update'].message_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_customer__extension__setting__pb2._CUSTOMEREXTENSIONSETTING
_CUSTOMEREXTENSIONSETTINGOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['create'])
_CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['create'].containing_oneof = _CUSTOMEREXTENSIONSETTINGOPERATION.oneofs_by_name['operation']
_CUSTOMEREXTENSIONSETTINGOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['update'])
_CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['update'].containing_oneof = _CUSTOMEREXTENSIONSETTINGOPERATION.oneofs_by_name['operation']
_CUSTOMEREXTENSIONSETTINGOPERATION.oneofs_by_name['operation'].fields.append(
  _CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['remove'])
_CUSTOMEREXTENSIONSETTINGOPERATION.fields_by_name['remove'].containing_oneof = _CUSTOMEREXTENSIONSETTINGOPERATION.oneofs_by_name['operation']
_MUTATECUSTOMEREXTENSIONSETTINGSRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATECUSTOMEREXTENSIONSETTINGSRESPONSE.fields_by_name['results'].message_type = _MUTATECUSTOMEREXTENSIONSETTINGRESULT
DESCRIPTOR.message_types_by_name['GetCustomerExtensionSettingRequest'] = _GETCUSTOMEREXTENSIONSETTINGREQUEST
DESCRIPTOR.message_types_by_name['MutateCustomerExtensionSettingsRequest'] = _MUTATECUSTOMEREXTENSIONSETTINGSREQUEST
DESCRIPTOR.message_types_by_name['CustomerExtensionSettingOperation'] = _CUSTOMEREXTENSIONSETTINGOPERATION
DESCRIPTOR.message_types_by_name['MutateCustomerExtensionSettingsResponse'] = _MUTATECUSTOMEREXTENSIONSETTINGSRESPONSE
DESCRIPTOR.message_types_by_name['MutateCustomerExtensionSettingResult'] = _MUTATECUSTOMEREXTENSIONSETTINGRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetCustomerExtensionSettingRequest = _reflection.GeneratedProtocolMessageType('GetCustomerExtensionSettingRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETCUSTOMEREXTENSIONSETTINGREQUEST,
  __module__ = 'google.ads.googleads_v2.proto.services.customer_extension_setting_service_pb2'
  ,
  __doc__ = """Request message for
  [CustomerExtensionSettingService.GetCustomerExtensionSetting][google.ads.googleads.v2.services.CustomerExtensionSettingService.GetCustomerExtensionSetting].
  
  
  Attributes:
      resource_name:
          The resource name of the customer extension setting to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.GetCustomerExtensionSettingRequest)
  ))
_sym_db.RegisterMessage(GetCustomerExtensionSettingRequest)

MutateCustomerExtensionSettingsRequest = _reflection.GeneratedProtocolMessageType('MutateCustomerExtensionSettingsRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMEREXTENSIONSETTINGSREQUEST,
  __module__ = 'google.ads.googleads_v2.proto.services.customer_extension_setting_service_pb2'
  ,
  __doc__ = """Request message for
  [CustomerExtensionSettingService.MutateCustomerExtensionSettings][google.ads.googleads.v2.services.CustomerExtensionSettingService.MutateCustomerExtensionSettings].
  
  
  Attributes:
      customer_id:
          The ID of the customer whose customer extension settings are
          being modified.
      operations:
          The list of operations to perform on individual customer
          extension settings.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.MutateCustomerExtensionSettingsRequest)
  ))
_sym_db.RegisterMessage(MutateCustomerExtensionSettingsRequest)

CustomerExtensionSettingOperation = _reflection.GeneratedProtocolMessageType('CustomerExtensionSettingOperation', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMEREXTENSIONSETTINGOPERATION,
  __module__ = 'google.ads.googleads_v2.proto.services.customer_extension_setting_service_pb2'
  ,
  __doc__ = """A single operation (create, update, remove) on a customer extension
  setting.
  
  
  Attributes:
      update_mask:
          FieldMask that determines which resource fields are modified
          in an update.
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new
          customer extension setting.
      update:
          Update operation: The customer extension setting is expected
          to have a valid resource name.
      remove:
          Remove operation: A resource name for the removed customer
          extension setting is expected, in this format:  ``customers/{c
          ustomer_id}/customerExtensionSettings/{extension_type}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.CustomerExtensionSettingOperation)
  ))
_sym_db.RegisterMessage(CustomerExtensionSettingOperation)

MutateCustomerExtensionSettingsResponse = _reflection.GeneratedProtocolMessageType('MutateCustomerExtensionSettingsResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMEREXTENSIONSETTINGSRESPONSE,
  __module__ = 'google.ads.googleads_v2.proto.services.customer_extension_setting_service_pb2'
  ,
  __doc__ = """Response message for a customer extension setting mutate.
  
  
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
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.MutateCustomerExtensionSettingsResponse)
  ))
_sym_db.RegisterMessage(MutateCustomerExtensionSettingsResponse)

MutateCustomerExtensionSettingResult = _reflection.GeneratedProtocolMessageType('MutateCustomerExtensionSettingResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATECUSTOMEREXTENSIONSETTINGRESULT,
  __module__ = 'google.ads.googleads_v2.proto.services.customer_extension_setting_service_pb2'
  ,
  __doc__ = """The result for the customer extension setting mutate.
  
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.MutateCustomerExtensionSettingResult)
  ))
_sym_db.RegisterMessage(MutateCustomerExtensionSettingResult)


DESCRIPTOR._options = None

_CUSTOMEREXTENSIONSETTINGSERVICE = _descriptor.ServiceDescriptor(
  name='CustomerExtensionSettingService',
  full_name='google.ads.googleads.v2.services.CustomerExtensionSettingService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=1091,
  serialized_end=1645,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetCustomerExtensionSetting',
    full_name='google.ads.googleads.v2.services.CustomerExtensionSettingService.GetCustomerExtensionSetting',
    index=0,
    containing_service=None,
    input_type=_GETCUSTOMEREXTENSIONSETTINGREQUEST,
    output_type=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_customer__extension__setting__pb2._CUSTOMEREXTENSIONSETTING,
    serialized_options=_b('\202\323\344\223\002=\022;/v2/{resource_name=customers/*/customerExtensionSettings/*}'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateCustomerExtensionSettings',
    full_name='google.ads.googleads.v2.services.CustomerExtensionSettingService.MutateCustomerExtensionSettings',
    index=1,
    containing_service=None,
    input_type=_MUTATECUSTOMEREXTENSIONSETTINGSREQUEST,
    output_type=_MUTATECUSTOMEREXTENSIONSETTINGSRESPONSE,
    serialized_options=_b('\202\323\344\223\002C\">/v2/customers/{customer_id=*}/customerExtensionSettings:mutate:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_CUSTOMEREXTENSIONSETTINGSERVICE)

DESCRIPTOR.services_by_name['CustomerExtensionSettingService'] = _CUSTOMEREXTENSIONSETTINGSERVICE

# @@protoc_insertion_point(module_scope)
