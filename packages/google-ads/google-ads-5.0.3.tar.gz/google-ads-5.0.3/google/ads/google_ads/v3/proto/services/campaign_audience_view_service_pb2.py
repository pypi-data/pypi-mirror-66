# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v3/proto/services/campaign_audience_view_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v3.proto.resources import campaign_audience_view_pb2 as google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_campaign__audience__view__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v3/proto/services/campaign_audience_view_service.proto',
  package='google.ads.googleads.v3.services',
  syntax='proto3',
  serialized_options=_b('\n$com.google.ads.googleads.v3.servicesB CampaignAudienceViewServiceProtoP\001ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v3/services;services\242\002\003GAA\252\002 Google.Ads.GoogleAds.V3.Services\312\002 Google\\Ads\\GoogleAds\\V3\\Services\352\002$Google::Ads::GoogleAds::V3::Services'),
  serialized_pb=_b('\nKgoogle/ads/googleads_v3/proto/services/campaign_audience_view_service.proto\x12 google.ads.googleads.v3.services\x1a\x44google/ads/googleads_v3/proto/resources/campaign_audience_view.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\"<\n\x1eGetCampaignAudienceViewRequest\x12\x1a\n\rresource_name\x18\x01 \x01(\tB\x03\xe0\x41\x02\x32\xa2\x02\n\x1b\x43\x61mpaignAudienceViewService\x12\xe5\x01\n\x17GetCampaignAudienceView\x12@.google.ads.googleads.v3.services.GetCampaignAudienceViewRequest\x1a\x37.google.ads.googleads.v3.resources.CampaignAudienceView\"O\x82\xd3\xe4\x93\x02\x39\x12\x37/v3/{resource_name=customers/*/campaignAudienceViews/*}\xda\x41\rresource_name\x1a\x1b\xca\x41\x18googleads.googleapis.comB\x87\x02\n$com.google.ads.googleads.v3.servicesB CampaignAudienceViewServiceProtoP\x01ZHgoogle.golang.org/genproto/googleapis/ads/googleads/v3/services;services\xa2\x02\x03GAA\xaa\x02 Google.Ads.GoogleAds.V3.Services\xca\x02 Google\\Ads\\GoogleAds\\V3\\Services\xea\x02$Google::Ads::GoogleAds::V3::Servicesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_campaign__audience__view__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_api_dot_client__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,])




_GETCAMPAIGNAUDIENCEVIEWREQUEST = _descriptor.Descriptor(
  name='GetCampaignAudienceViewRequest',
  full_name='google.ads.googleads.v3.services.GetCampaignAudienceViewRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v3.services.GetCampaignAudienceViewRequest.resource_name', index=0,
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
  serialized_start=271,
  serialized_end=331,
)

DESCRIPTOR.message_types_by_name['GetCampaignAudienceViewRequest'] = _GETCAMPAIGNAUDIENCEVIEWREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetCampaignAudienceViewRequest = _reflection.GeneratedProtocolMessageType('GetCampaignAudienceViewRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETCAMPAIGNAUDIENCEVIEWREQUEST,
  __module__ = 'google.ads.googleads_v3.proto.services.campaign_audience_view_service_pb2'
  ,
  __doc__ = """Request message for
  [CampaignAudienceViewService.GetCampaignAudienceView][google.ads.googleads.v3.services.CampaignAudienceViewService.GetCampaignAudienceView].
  
  
  Attributes:
      resource_name:
          Required. The resource name of the campaign audience view to
          fetch.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v3.services.GetCampaignAudienceViewRequest)
  ))
_sym_db.RegisterMessage(GetCampaignAudienceViewRequest)


DESCRIPTOR._options = None
_GETCAMPAIGNAUDIENCEVIEWREQUEST.fields_by_name['resource_name']._options = None

_CAMPAIGNAUDIENCEVIEWSERVICE = _descriptor.ServiceDescriptor(
  name='CampaignAudienceViewService',
  full_name='google.ads.googleads.v3.services.CampaignAudienceViewService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=_b('\312A\030googleads.googleapis.com'),
  serialized_start=334,
  serialized_end=624,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetCampaignAudienceView',
    full_name='google.ads.googleads.v3.services.CampaignAudienceViewService.GetCampaignAudienceView',
    index=0,
    containing_service=None,
    input_type=_GETCAMPAIGNAUDIENCEVIEWREQUEST,
    output_type=google_dot_ads_dot_googleads__v3_dot_proto_dot_resources_dot_campaign__audience__view__pb2._CAMPAIGNAUDIENCEVIEW,
    serialized_options=_b('\202\323\344\223\0029\0227/v3/{resource_name=customers/*/campaignAudienceViews/*}\332A\rresource_name'),
  ),
])
_sym_db.RegisterServiceDescriptor(_CAMPAIGNAUDIENCEVIEWSERVICE)

DESCRIPTOR.services_by_name['CampaignAudienceViewService'] = _CAMPAIGNAUDIENCEVIEWSERVICE

# @@protoc_insertion_point(module_scope)
