# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.ads.google_ads.v2.proto.services import payments_account_service_pb2 as google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_payments__account__service__pb2


class PaymentsAccountServiceStub(object):
  """Proto file describing the payments account service.

  Service to provide payments accounts that can be used to set up consolidated
  billing.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ListPaymentsAccounts = channel.unary_unary(
        '/google.ads.googleads.v2.services.PaymentsAccountService/ListPaymentsAccounts',
        request_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_payments__account__service__pb2.ListPaymentsAccountsRequest.SerializeToString,
        response_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_payments__account__service__pb2.ListPaymentsAccountsResponse.FromString,
        )


class PaymentsAccountServiceServicer(object):
  """Proto file describing the payments account service.

  Service to provide payments accounts that can be used to set up consolidated
  billing.
  """

  def ListPaymentsAccounts(self, request, context):
    """Returns all payments accounts associated with all managers
    between the login customer ID and specified serving customer in the
    hierarchy, inclusive.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PaymentsAccountServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ListPaymentsAccounts': grpc.unary_unary_rpc_method_handler(
          servicer.ListPaymentsAccounts,
          request_deserializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_payments__account__service__pb2.ListPaymentsAccountsRequest.FromString,
          response_serializer=google_dot_ads_dot_googleads__v2_dot_proto_dot_services_dot_payments__account__service__pb2.ListPaymentsAccountsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.ads.googleads.v2.services.PaymentsAccountService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
