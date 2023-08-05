# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v1.proto.resources import search_term_view_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_search__term__view__pb2
from google.ads.google_ads.v1.proto.services import search_term_view_service_pb2 as google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_search__term__view__service__pb2


class SearchTermViewServiceStub(object):
  """Proto file describing the Search Term View service.

  Service to manage search term views.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetSearchTermView = channel.unary_unary(
        '/google.ads.googleads.v1.services.SearchTermViewService/GetSearchTermView',
        request_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_search__term__view__service__pb2.GetSearchTermViewRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_search__term__view__pb2.SearchTermView.FromString,
        )


class SearchTermViewServiceServicer(object):
  """Proto file describing the Search Term View service.

  Service to manage search term views.
  """

  def GetSearchTermView(self, request, context):
    """Returns the attributes of the requested search term view.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SearchTermViewServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetSearchTermView': grpc.unary_unary_rpc_method_handler(
          servicer.GetSearchTermView,
          request_deserializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_services_dot_search__term__view__service__pb2.GetSearchTermViewRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v1_dot_proto_dot_resources_dot_search__term__view__pb2.SearchTermView.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v1.services.SearchTermViewService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
