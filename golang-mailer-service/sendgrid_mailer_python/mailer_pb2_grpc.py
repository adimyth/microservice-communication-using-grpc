# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import sendgrid_mailer_python.mailer_pb2 as mailer__pb2


class MailerServiceStub(object):
    """service is a collection of RPC methods.
    RPC methods accept a single request message and return a single response message.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendMails = channel.unary_unary(
            "/mailer.MailerService/SendMails",
            request_serializer=mailer__pb2.SendMailRequest.SerializeToString,
            response_deserializer=mailer__pb2.SendMailResponse.FromString,
        )


class MailerServiceServicer(object):
    """service is a collection of RPC methods.
    RPC methods accept a single request message and return a single response message.
    """

    def SendMails(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_MailerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "SendMails": grpc.unary_unary_rpc_method_handler(
            servicer.SendMails,
            request_deserializer=mailer__pb2.SendMailRequest.FromString,
            response_serializer=mailer__pb2.SendMailResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "mailer.MailerService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class MailerService(object):
    """service is a collection of RPC methods.
    RPC methods accept a single request message and return a single response message.
    """

    @staticmethod
    def SendMails(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/mailer.MailerService/SendMails",
            mailer__pb2.SendMailRequest.SerializeToString,
            mailer__pb2.SendMailResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
