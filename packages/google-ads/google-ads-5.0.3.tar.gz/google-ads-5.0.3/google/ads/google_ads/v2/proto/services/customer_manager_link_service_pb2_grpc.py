# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v2.proto.resources import customer_manager_link_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_customer__manager__link__pb2
from google.ads.google_ads.v2.proto.services import customer_manager_link_service_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_customer__manager__link__service__pb2


class CustomerManagerLinkServiceStub(object):
  """Service to manage customer-manager links.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetCustomerManagerLink = channel.unary_unary(
        '/google.ads.googleads.v2.services.CustomerManagerLinkService/GetCustomerManagerLink',
        request_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_customer__manager__link__service__pb2.GetCustomerManagerLinkRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_customer__manager__link__pb2.CustomerManagerLink.FromString,
        )
    self.MutateCustomerManagerLink = channel.unary_unary(
        '/google.ads.googleads.v2.services.CustomerManagerLinkService/MutateCustomerManagerLink',
        request_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_customer__manager__link__service__pb2.MutateCustomerManagerLinkRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_customer__manager__link__service__pb2.MutateCustomerManagerLinkResponse.FromString,
        )


class CustomerManagerLinkServiceServicer(object):
  """Service to manage customer-manager links.
  """

  def GetCustomerManagerLink(self, request, context):
    """Returns the requested CustomerManagerLink in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MutateCustomerManagerLink(self, request, context):
    """Creates or updates customer manager links. Operation statuses are returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CustomerManagerLinkServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetCustomerManagerLink': grpc.unary_unary_rpc_method_handler(
          servicer.GetCustomerManagerLink,
          request_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_customer__manager__link__service__pb2.GetCustomerManagerLinkRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_customer__manager__link__pb2.CustomerManagerLink.SerializeToString,
      ),
      'MutateCustomerManagerLink': grpc.unary_unary_rpc_method_handler(
          servicer.MutateCustomerManagerLink,
          request_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_customer__manager__link__service__pb2.MutateCustomerManagerLinkRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_customer__manager__link__service__pb2.MutateCustomerManagerLinkResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v2.services.CustomerManagerLinkService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
