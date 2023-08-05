# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/services/extension_feed_item_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v2.proto.resources import extension_feed_item_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_extension__feed__item__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v2/proto/services/extension_feed_item_service.proto',
  package='google.ads.googleads.v2.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v2.servicesB\035ExtensionFeedItemServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v2/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V2.Services\312\002 Google\\Ads\\GoogleAds\\V2\\Services\352\002$Google::Ads::GoogleAds::V2::Services'),
  serialized_pb=_b('\nHgoogle/ads/googleads_v2/proto/services/extension_feed_item_service.proto\x12 google.ads.googleads.v2.services\x1a\x41google/ads/googleads_v2/proto/resources/extension_feed_item.proto\x1a\x1cgoogle/api/annotations.proto\x1a google/protobuf/field_mask.proto\x1a\x17google/rpc/status.proto\x1a\x17google/api/client.proto\"4\n\x1bGetExtensionFeedItemRequest\x12\x15\n\rresource_name\x18\x01 \x01(\t\"\xb8\x01\n\x1fMutateExtensionFeedItemsRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\t\x12P\n\noperations\x18\x02 \x03(\x0b\x32<.google.ads.googleads.v2.services.ExtensionFeedItemOperation\x12\x17\n\x0fpartial_failure\x18\x03 \x01(\x08\x12\x15\n\rvalidate_only\x18\x04 \x01(\x08\"\xfc\x01\n\x1a\x45xtensionFeedItemOperation\x12/\n\x0bupdate_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x46\n\x06\x63reate\x18\x01 \x01(\x0b\x32\x34.google.ads.googleads.v2.resources.ExtensionFeedItemH\x00\x12\x46\n\x06update\x18\x02 \x01(\x0b\x32\x34.google.ads.googleads.v2.resources.ExtensionFeedItemH\x00\x12\x10\n\x06remove\x18\x03 \x01(\tH\x00\x42\x0b\n\toperation\"\xa7\x01\n MutateExtensionFeedItemsResponse\x12\x31\n\x15partial_failure_error\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\x12P\n\x07results\x18\x02 \x03(\x0b\x32?.google.ads.googleads.v2.services.MutateExtensionFeedItemResult\"6\n\x1dMutateExtensionFeedItemResult\x12\x15\n\rresource_name\x18\x01 \x01(\t2\xeb\x03\n\x18\x45xtensionFeedItemService\x12\xc9\x01\n\x14GetExtensionFeedItem\x12=.google.ads.googleads.v2.services.GetExtensionFeedItemRequest\x1a\x34.google.ads.googleads.v2.resources.ExtensionFeedItem\"<\x82\xd3\xe4\x93\x02\x36\x12\x34/v2/{resource_name=customers/*/extensionFeedItems/*}\x12\xe5\x01\n\x18MutateExtensionFeedItems\x12\x41.google.ads.googleads.v2.services.MutateExtensionFeedItemsRequest\x1a\x42.google.ads.googleads.v2.services.MutateExtensionFeedItemsResponse\"B\x82\xd3\xe4\x93\x02<\"7/v2/customers/{customer_id=*}/extensionFeedItems:mutate:\x01*\x1a\x1b\xca\x41\x18googleads.googleapis.comB\x84\x02\n$com.google.ads.googleads.v2.servicesB\x1d\x45xtensionFeedItemServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v2/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V2.Services\xca\x02 Google\\Ads\\GoogleAds\\V2\\Services\xea\x02$Google::Ads::GoogleAds::V2::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_extension__feed__item__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,google_dot_rpc_dot_status__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,])




_GETEXTENSIONFEEDITEMREQUEST = _descriptor.Descriptor(
  name='GetExtensionFeedItemRequest',
  full_name='google.ads.googleads.v2.services.GetExtensionFeedItemRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.services.GetExtensionFeedItemRequest.resource_name', index=0,
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
  serialized_start=291,
  serialized_end=343,
)


_MUTATEEXTENSIONFEEDITEMSREQUEST = _descriptor.Descriptor(
  name='MutateExtensionFeedItemsRequest',
  full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer_id', full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemsRequest.customer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operations', full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemsRequest.operations', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='partial_failure', full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemsRequest.partial_failure', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='validate_only', full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemsRequest.validate_only', index=3,
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
  serialized_start=346,
  serialized_end=530,
)


_EXTENSIONFEEDITEMOPERATION = _descriptor.Descriptor(
  name='ExtensionFeedItemOperation',
  full_name='google.ads.googleads.v2.services.ExtensionFeedItemOperation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='google.ads.googleads.v2.services.ExtensionFeedItemOperation.update_mask', index=0,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='create', full_name='google.ads.googleads.v2.services.ExtensionFeedItemOperation.create', index=1,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='update', full_name='google.ads.googleads.v2.services.ExtensionFeedItemOperation.update', index=2,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='remove', full_name='google.ads.googleads.v2.services.ExtensionFeedItemOperation.remove', index=3,
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
      name='operation', full_name='google.ads.googleads.v2.services.ExtensionFeedItemOperation.operation',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=533,
  serialized_end=785,
)


_MUTATEEXTENSIONFEEDITEMSRESPONSE = _descriptor.Descriptor(
  name='MutateExtensionFeedItemsResponse',
  full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='partial_failure_error', full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemsResponse.partial_failure_error', index=0,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemsResponse.results', index=1,
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
  serialized_start=788,
  serialized_end=955,
)


_MUTATEEXTENSIONFEEDITEMRESULT = _descriptor.Descriptor(
  name='MutateExtensionFeedItemResult',
  full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.services.MutateExtensionFeedItemResult.resource_name', index=0,
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
  serialized_start=957,
  serialized_end=1011,
)

_MUTATEEXTENSIONFEEDITEMSREQUEST.fields_by_name['operations'].message_type = _EXTENSIONFEEDITEMOPERATION
_EXTENSIONFEEDITEMOPERATION.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_EXTENSIONFEEDITEMOPERATION.fields_by_name['create'].message_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_extension__feed__item__pb2._EXTENSIONFEEDITEM
_EXTENSIONFEEDITEMOPERATION.fields_by_name['update'].message_type = google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_extension__feed__item__pb2._EXTENSIONFEEDITEM
_EXTENSIONFEEDITEMOPERATION.oneofs_by_name['operation'].fields.append(
  _EXTENSIONFEEDITEMOPERATION.fields_by_name['create'])
_EXTENSIONFEEDITEMOPERATION.fields_by_name['create'].containing_oneof = _EXTENSIONFEEDITEMOPERATION.oneofs_by_name['operation']
_EXTENSIONFEEDITEMOPERATION.oneofs_by_name['operation'].fields.append(
  _EXTENSIONFEEDITEMOPERATION.fields_by_name['update'])
_EXTENSIONFEEDITEMOPERATION.fields_by_name['update'].containing_oneof = _EXTENSIONFEEDITEMOPERATION.oneofs_by_name['operation']
_EXTENSIONFEEDITEMOPERATION.oneofs_by_name['operation'].fields.append(
  _EXTENSIONFEEDITEMOPERATION.fields_by_name['remove'])
_EXTENSIONFEEDITEMOPERATION.fields_by_name['remove'].containing_oneof = _EXTENSIONFEEDITEMOPERATION.oneofs_by_name['operation']
_MUTATEEXTENSIONFEEDITEMSRESPONSE.fields_by_name['partial_failure_error'].message_type = google_dot_rpc_dot_status__pb2._STATUS
_MUTATEEXTENSIONFEEDITEMSRESPONSE.fields_by_name['results'].message_type = _MUTATEEXTENSIONFEEDITEMRESULT
DESCRIPTOR.message_types_by_name['GetExtensionFeedItemRequest'] = _GETEXTENSIONFEEDITEMREQUEST
DESCRIPTOR.message_types_by_name['MutateExtensionFeedItemsRequest'] = _MUTATEEXTENSIONFEEDITEMSREQUEST
DESCRIPTOR.message_types_by_name['ExtensionFeedItemOperation'] = _EXTENSIONFEEDITEMOPERATION
DESCRIPTOR.message_types_by_name['MutateExtensionFeedItemsResponse'] = _MUTATEEXTENSIONFEEDITEMSRESPONSE
DESCRIPTOR.message_types_by_name['MutateExtensionFeedItemResult'] = _MUTATEEXTENSIONFEEDITEMRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetExtensionFeedItemRequest = _reflection.GeneratedProtocolMessageType('GetExtensionFeedItemRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETEXTENSIONFEEDITEMREQUEST,
  __module__ = 'google.ads.googleads_v2.proto.services.extension_feed_item_service_pb2'
  ,
  __doc__ = """Request message for
  [ExtensionFeedItemService.GetExtensionFeedItem][google.ads.googleads.v2.services.ExtensionFeedItemService.GetExtensionFeedItem].
  
  
  Attributes:
      resource_name:
          The resource name of the extension feed item to fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.GetExtensionFeedItemRequest)
  ))
_sym_db.RegisterMessage(GetExtensionFeedItemRequest)

MutateExtensionFeedItemsRequest = _reflection.GeneratedProtocolMessageType('MutateExtensionFeedItemsRequest', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEEXTENSIONFEEDITEMSREQUEST,
  __module__ = 'google.ads.googleads_v2.proto.services.extension_feed_item_service_pb2'
  ,
  __doc__ = """Request message for
  [ExtensionFeedItemService.MutateExtensionFeedItems][google.ads.googleads.v2.services.ExtensionFeedItemService.MutateExtensionFeedItems].
  
  
  Attributes:
      customer_id:
          The ID of the customer whose extension feed items are being
          modified.
      operations:
          The list of operations to perform on individual extension feed
          items.
      partial_failure:
          If true, successful operations will be carried out and invalid
          operations will return errors. If false, all operations will
          be carried out in one transaction if and only if they are all
          valid. Default is false.
      validate_only:
          If true, the request is validated but not executed. Only
          errors are returned, not results.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.MutateExtensionFeedItemsRequest)
  ))
_sym_db.RegisterMessage(MutateExtensionFeedItemsRequest)

ExtensionFeedItemOperation = _reflection.GeneratedProtocolMessageType('ExtensionFeedItemOperation', (_message.Message,), dict(
  DESCRIPTOR = _EXTENSIONFEEDITEMOPERATION,
  __module__ = 'google.ads.googleads_v2.proto.services.extension_feed_item_service_pb2'
  ,
  __doc__ = """A single operation (create, update, remove) on an extension feed item.
  
  
  Attributes:
      update_mask:
          FieldMask that determines which resource fields are modified
          in an update.
      operation:
          The mutate operation.
      create:
          Create operation: No resource name is expected for the new
          extension feed item.
      update:
          Update operation: The extension feed item is expected to have
          a valid resource name.
      remove:
          Remove operation: A resource name for the removed extension
          feed item is expected, in this format:
          ``customers/{customer_id}/extensionFeedItems/{feed_item_id}``
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.ExtensionFeedItemOperation)
  ))
_sym_db.RegisterMessage(ExtensionFeedItemOperation)

MutateExtensionFeedItemsResponse = _reflection.GeneratedProtocolMessageType('MutateExtensionFeedItemsResponse', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEEXTENSIONFEEDITEMSRESPONSE,
  __module__ = 'google.ads.googleads_v2.proto.services.extension_feed_item_service_pb2'
  ,
  __doc__ = """Response message for an extension feed item mutate.
  
  
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
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.MutateExtensionFeedItemsResponse)
  ))
_sym_db.RegisterMessage(MutateExtensionFeedItemsResponse)

MutateExtensionFeedItemResult = _reflection.GeneratedProtocolMessageType('MutateExtensionFeedItemResult', (_message.Message,), dict(
  DESCRIPTOR = _MUTATEEXTENSIONFEEDITEMRESULT,
  __module__ = 'google.ads.googleads_v2.proto.services.extension_feed_item_service_pb2'
  ,
  __doc__ = """The result for the extension feed item mutate.
  
  
  Attributes:
      resource_name:
          Returned for successful operations.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.services.MutateExtensionFeedItemResult)
  ))
_sym_db.RegisterMessage(MutateExtensionFeedItemResult)


DESCRIPTOR._options = None

_EXTENSIONFEEDITEMSERVICE = _descriptor.ServiceDescriptor(
  name='ExtensionFeedItemService',
  full_name='google.ads.googleads.v2.services.ExtensionFeedItemService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=1014,
  serialized_end=1505,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetExtensionFeedItem',
    full_name='google.ads.googleads.v2.services.ExtensionFeedItemService.GetExtensionFeedItem',
    index=0,
    containing_service=None,
    input_type=_GETEXTENSIONFEEDITEMREQUEST,
    output_type=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_extension__feed__item__pb2._EXTENSIONFEEDITEM,
    serialized_options=_b('\202\323\344\223\0026\0224/v2/{resource_name=customers/*/extensionFeedItems/*}'),
  ),
  _descriptor.MethodDescriptor(
    name='MutateExtensionFeedItems',
    full_name='google.ads.googleads.v2.services.ExtensionFeedItemService.MutateExtensionFeedItems',
    index=1,
    containing_service=None,
    input_type=_MUTATEEXTENSIONFEEDITEMSREQUEST,
    output_type=_MUTATEEXTENSIONFEEDITEMSRESPONSE,
    serialized_options=_b('\202\323\344\223\002<\"7/v2/customers/{customer_id=*}/extensionFeedItems:mutate:\001*'),
  ),
])
_sym_db.RegisterServiceDescriptor(_EXTENSIONFEEDITEMSERVICE)

DESCRIPTOR.services_by_name['ExtensionFeedItemService'] = _EXTENSIONFEEDITEMSERVICE

# @@protoc_insertion_point(module_scope)
