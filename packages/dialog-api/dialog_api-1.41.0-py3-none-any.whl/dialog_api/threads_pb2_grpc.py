# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import miscellaneous_pb2 as miscellaneous__pb2
from . import threads_pb2 as threads__pb2


class ThreadsStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateThread = channel.unary_unary(
                '/dialog.Threads/CreateThread',
                request_serializer=threads__pb2.RequestCreateThread.SerializeToString,
                response_deserializer=threads__pb2.ResponseCreateThread.FromString,
                )
        self.LiftThread = channel.unary_unary(
                '/dialog.Threads/LiftThread',
                request_serializer=threads__pb2.RequestLiftThread.SerializeToString,
                response_deserializer=threads__pb2.ResponseLiftThread.FromString,
                )
        self.LoadGroupThreads = channel.unary_unary(
                '/dialog.Threads/LoadGroupThreads',
                request_serializer=threads__pb2.RequestLoadGroupThreads.SerializeToString,
                response_deserializer=threads__pb2.ResponseLoadGroupThreads.FromString,
                )
        self.JoinThread = channel.unary_unary(
                '/dialog.Threads/JoinThread',
                request_serializer=threads__pb2.RequestJoinThread.SerializeToString,
                response_deserializer=miscellaneous__pb2.ResponseVoid.FromString,
                )


class ThreadsServicer(object):
    """Missing associated documentation comment in .proto file"""

    def CreateThread(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LiftThread(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoadGroupThreads(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinThread(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ThreadsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateThread': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateThread,
                    request_deserializer=threads__pb2.RequestCreateThread.FromString,
                    response_serializer=threads__pb2.ResponseCreateThread.SerializeToString,
            ),
            'LiftThread': grpc.unary_unary_rpc_method_handler(
                    servicer.LiftThread,
                    request_deserializer=threads__pb2.RequestLiftThread.FromString,
                    response_serializer=threads__pb2.ResponseLiftThread.SerializeToString,
            ),
            'LoadGroupThreads': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadGroupThreads,
                    request_deserializer=threads__pb2.RequestLoadGroupThreads.FromString,
                    response_serializer=threads__pb2.ResponseLoadGroupThreads.SerializeToString,
            ),
            'JoinThread': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinThread,
                    request_deserializer=threads__pb2.RequestJoinThread.FromString,
                    response_serializer=miscellaneous__pb2.ResponseVoid.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dialog.Threads', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Threads(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def CreateThread(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.Threads/CreateThread',
            threads__pb2.RequestCreateThread.SerializeToString,
            threads__pb2.ResponseCreateThread.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LiftThread(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.Threads/LiftThread',
            threads__pb2.RequestLiftThread.SerializeToString,
            threads__pb2.ResponseLiftThread.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LoadGroupThreads(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.Threads/LoadGroupThreads',
            threads__pb2.RequestLoadGroupThreads.SerializeToString,
            threads__pb2.ResponseLoadGroupThreads.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def JoinThread(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.Threads/JoinThread',
            threads__pb2.RequestJoinThread.SerializeToString,
            miscellaneous__pb2.ResponseVoid.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
