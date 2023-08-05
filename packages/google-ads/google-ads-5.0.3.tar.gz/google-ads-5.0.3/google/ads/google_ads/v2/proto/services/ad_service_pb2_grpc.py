# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v2.proto.resources import ad_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_ad__pb2
from google.ads.google_ads.v2.proto.services import ad_service_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_ad__service__pb2


class AdServiceStub(object):
  """Proto file describing the  Ad service.

  Service to manage ads.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetAd = channel.unary_unary(
        '/google.ads.googleads.v2.services.AdService/GetAd',
        request_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_ad__service__pb2.GetAdRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_ad__pb2.Ad.FromString,
        )
    self.MutateAds = channel.unary_unary(
        '/google.ads.googleads.v2.services.AdService/MutateAds',
        request_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_ad__service__pb2.MutateAdsRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_ad__service__pb2.MutateAdsResponse.FromString,
        )


class AdServiceServicer(object):
  """Proto file describing the  Ad service.

  Service to manage ads.
  """

  def GetAd(self, request, context):
    """Returns the requested ad in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def MutateAds(self, request, context):
    """Updates ads. Operation statuses are returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AdServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetAd': grpc.unary_unary_rpc_method_handler(
          servicer.GetAd,
          request_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_ad__service__pb2.GetAdRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_ad__pb2.Ad.SerializeToString,
      ),
      'MutateAds': grpc.unary_unary_rpc_method_handler(
          servicer.MutateAds,
          request_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_ad__service__pb2.MutateAdsRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_ad__service__pb2.MutateAdsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v2.services.AdService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
