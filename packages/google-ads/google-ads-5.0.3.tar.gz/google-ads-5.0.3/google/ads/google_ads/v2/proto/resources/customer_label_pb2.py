# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v2/proto/resources/customer_label.proto

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
  name='google/ads/googleads_v2/proto/resources/customer_label.proto',
  package='google.ads.googleads.v2.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v2.resourcesB\022CustomerLabelProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v2/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V2.Resources\312\002!Google\\Ads\\GoogleAds\\V2\\Resources\352\002%Google::Ads::GoogleAds::V2::Resources'),
  serialized_pb=_b('\n<google/ads/googleads_v2/proto/resources/customer_label.proto\x12!google.ads.googleads.v2.resources\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\x83\x01\n\rCustomerLabel\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12.\n\x08\x63ustomer\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValue\x12+\n\x05label\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\xff\x01\n%com.google.ads.googleads.v2.resourcesB\x12\x43ustomerLabelProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v2/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V2.Resources\xca\x02!Google\\Ads\\GoogleAds\\V2\\Resources\xea\x02%Google::Ads::GoogleAds::V2::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_CUSTOMERLABEL = _descriptor.Descriptor(
  name='CustomerLabel',
  full_name='google.ads.googleads.v2.resources.CustomerLabel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v2.resources.CustomerLabel.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='customer', full_name='google.ads.googleads.v2.resources.CustomerLabel.customer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='label', full_name='google.ads.googleads.v2.resources.CustomerLabel.label', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=162,
  serialized_end=293,
)

_CUSTOMERLABEL.fields_by_name['customer'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CUSTOMERLABEL.fields_by_name['label'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
DESCRIPTOR.message_types_by_name['CustomerLabel'] = _CUSTOMERLABEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CustomerLabel = _reflection.GeneratedProtocolMessageType('CustomerLabel', (_message.Message,), dict(
  DESCRIPTOR = _CUSTOMERLABEL,
  __module__ = 'google.ads.googleads_v2.proto.resources.customer_label_pb2'
  ,
  __doc__ = """Represents a relationship between a customer and a label. This customer
  may not have access to all the labels attached to it. Additional
  CustomerLabels may be returned by increasing permissions with
  login-customer-id.
  
  
  Attributes:
      resource_name:
          Name of the resource. Customer label resource names have the
          form: ``customers/{customer_id}/customerLabels/{label_id}``
      customer:
          The resource name of the customer to which the label is
          attached. Read only.
      label:
          The resource name of the label assigned to the customer.
          Note: the Customer ID portion of the label resource name is
          not validated when creating a new CustomerLabel.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v2.resources.CustomerLabel)
  ))
_sym_db.RegisterMessage(CustomerLabel)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
