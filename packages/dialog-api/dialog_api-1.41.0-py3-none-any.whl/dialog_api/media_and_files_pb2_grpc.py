# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import media_and_files_pb2 as media__and__files__pb2


class MediaAndFilesStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFileUrl = channel.unary_unary(
                '/dialog.MediaAndFiles/GetFileUrl',
                request_serializer=media__and__files__pb2.RequestGetFileUrl.SerializeToString,
                response_deserializer=media__and__files__pb2.ResponseGetFileUrl.FromString,
                )
        self.GetFileUrls = channel.unary_unary(
                '/dialog.MediaAndFiles/GetFileUrls',
                request_serializer=media__and__files__pb2.RequestGetFileUrls.SerializeToString,
                response_deserializer=media__and__files__pb2.ResponseGetFileUrls.FromString,
                )
        self.GetFileUrlBuilder = channel.unary_unary(
                '/dialog.MediaAndFiles/GetFileUrlBuilder',
                request_serializer=media__and__files__pb2.RequestGetFileUrlBuilder.SerializeToString,
                response_deserializer=media__and__files__pb2.ResponseGetFileUrlBuilder.FromString,
                )
        self.GetFileUploadUrl = channel.unary_unary(
                '/dialog.MediaAndFiles/GetFileUploadUrl',
                request_serializer=media__and__files__pb2.RequestGetFileUploadUrl.SerializeToString,
                response_deserializer=media__and__files__pb2.ResponseGetFileUploadUrl.FromString,
                )
        self.CommitFileUpload = channel.unary_unary(
                '/dialog.MediaAndFiles/CommitFileUpload',
                request_serializer=media__and__files__pb2.RequestCommitFileUpload.SerializeToString,
                response_deserializer=media__and__files__pb2.ResponseCommitFileUpload.FromString,
                )
        self.GetFileUploadPartUrl = channel.unary_unary(
                '/dialog.MediaAndFiles/GetFileUploadPartUrl',
                request_serializer=media__and__files__pb2.RequestGetFileUploadPartUrl.SerializeToString,
                response_deserializer=media__and__files__pb2.ResponseGetFileUploadPartUrl.FromString,
                )


class MediaAndFilesServicer(object):
    """Missing associated documentation comment in .proto file"""

    def GetFileUrl(self, request, context):
        """/ Get link to file for downloading
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileUrls(self, request, context):
        """/ Get link to files for downloading
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileUrlBuilder(self, request, context):
        """/ Create builder for file url
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileUploadUrl(self, request, context):
        """/ Get url for uploading
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CommitFileUpload(self, request, context):
        """/ Finish uploading a file
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileUploadPartUrl(self, request, context):
        """/ Get url for uploading chunk of file
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MediaAndFilesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFileUrl': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileUrl,
                    request_deserializer=media__and__files__pb2.RequestGetFileUrl.FromString,
                    response_serializer=media__and__files__pb2.ResponseGetFileUrl.SerializeToString,
            ),
            'GetFileUrls': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileUrls,
                    request_deserializer=media__and__files__pb2.RequestGetFileUrls.FromString,
                    response_serializer=media__and__files__pb2.ResponseGetFileUrls.SerializeToString,
            ),
            'GetFileUrlBuilder': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileUrlBuilder,
                    request_deserializer=media__and__files__pb2.RequestGetFileUrlBuilder.FromString,
                    response_serializer=media__and__files__pb2.ResponseGetFileUrlBuilder.SerializeToString,
            ),
            'GetFileUploadUrl': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileUploadUrl,
                    request_deserializer=media__and__files__pb2.RequestGetFileUploadUrl.FromString,
                    response_serializer=media__and__files__pb2.ResponseGetFileUploadUrl.SerializeToString,
            ),
            'CommitFileUpload': grpc.unary_unary_rpc_method_handler(
                    servicer.CommitFileUpload,
                    request_deserializer=media__and__files__pb2.RequestCommitFileUpload.FromString,
                    response_serializer=media__and__files__pb2.ResponseCommitFileUpload.SerializeToString,
            ),
            'GetFileUploadPartUrl': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileUploadPartUrl,
                    request_deserializer=media__and__files__pb2.RequestGetFileUploadPartUrl.FromString,
                    response_serializer=media__and__files__pb2.ResponseGetFileUploadPartUrl.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dialog.MediaAndFiles', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MediaAndFiles(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def GetFileUrl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.MediaAndFiles/GetFileUrl',
            media__and__files__pb2.RequestGetFileUrl.SerializeToString,
            media__and__files__pb2.ResponseGetFileUrl.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFileUrls(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.MediaAndFiles/GetFileUrls',
            media__and__files__pb2.RequestGetFileUrls.SerializeToString,
            media__and__files__pb2.ResponseGetFileUrls.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFileUrlBuilder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.MediaAndFiles/GetFileUrlBuilder',
            media__and__files__pb2.RequestGetFileUrlBuilder.SerializeToString,
            media__and__files__pb2.ResponseGetFileUrlBuilder.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFileUploadUrl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.MediaAndFiles/GetFileUploadUrl',
            media__and__files__pb2.RequestGetFileUploadUrl.SerializeToString,
            media__and__files__pb2.ResponseGetFileUploadUrl.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CommitFileUpload(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.MediaAndFiles/CommitFileUpload',
            media__and__files__pb2.RequestCommitFileUpload.SerializeToString,
            media__and__files__pb2.ResponseCommitFileUpload.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFileUploadPartUrl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dialog.MediaAndFiles/GetFileUploadPartUrl',
            media__and__files__pb2.RequestGetFileUploadPartUrl.SerializeToString,
            media__and__files__pb2.ResponseGetFileUploadPartUrl.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
