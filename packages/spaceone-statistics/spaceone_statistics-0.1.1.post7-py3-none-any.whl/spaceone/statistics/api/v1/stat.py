from spaceone.api.statistics.v1 import stat_pb2, stat_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class Stat(BaseAPI, stat_pb2_grpc.StatServicer):

    pb2 = stat_pb2
    pb2_grpc = stat_pb2_grpc

    def query(self, request, context):
        params, metadata = self.parse_request(request, context)
        with self.locator.get_service('StatService', metadata) as stat_service:
            return self.locator.get_info('StatInfo', stat_service.query(params))
