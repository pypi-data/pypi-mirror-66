# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v2.proto.resources import recommendation_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_recommendation__pb2
from google.ads.google_ads.v2.proto.services import recommendation_service_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2


class RecommendationServiceStub(object):
  """Proto file describing the Recommendation service.

  Service to manage recommendations.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetRecommendation = channel.unary_unary(
        '/google.ads.googleads.v2.services.RecommendationService/GetRecommendation',
        request_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.GetRecommendationRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_recommendation__pb2.Recommendation.FromString,
        )
    self.ApplyRecommendation = channel.unary_unary(
        '/google.ads.googleads.v2.services.RecommendationService/ApplyRecommendation',
        request_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.ApplyRecommendationRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.ApplyRecommendationResponse.FromString,
        )
    self.DismissRecommendation = channel.unary_unary(
        '/google.ads.googleads.v2.services.RecommendationService/DismissRecommendation',
        request_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.DismissRecommendationRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.DismissRecommendationResponse.FromString,
        )


class RecommendationServiceServicer(object):
  """Proto file describing the Recommendation service.

  Service to manage recommendations.
  """

  def GetRecommendation(self, request, context):
    """Returns the requested recommendation in full detail.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ApplyRecommendation(self, request, context):
    """Applies given recommendations with corresponding apply parameters.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DismissRecommendation(self, request, context):
    """Dismisses given recommendations.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RecommendationServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetRecommendation': grpc.unary_unary_rpc_method_handler(
          servicer.GetRecommendation,
          request_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.GetRecommendationRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_resources_dot_recommendation__pb2.Recommendation.SerializeToString,
      ),
      'ApplyRecommendation': grpc.unary_unary_rpc_method_handler(
          servicer.ApplyRecommendation,
          request_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.ApplyRecommendationRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.ApplyRecommendationResponse.SerializeToString,
      ),
      'DismissRecommendation': grpc.unary_unary_rpc_method_handler(
          servicer.DismissRecommendation,
          request_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.DismissRecommendationRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_recommendation__service__pb2.DismissRecommendationResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v2.services.RecommendationService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
