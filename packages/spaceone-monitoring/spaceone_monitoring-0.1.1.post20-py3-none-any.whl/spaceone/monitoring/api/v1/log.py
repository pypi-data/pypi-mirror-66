import time
from dateutil.parser import parse
from spaceone.api.monitoring.v1 import log_pb2, log_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class Log(BaseAPI, log_pb2_grpc.LogServicer):

    pb2 = log_pb2
    pb2_grpc = log_pb2_grpc

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)

        if 'start' in params:
            params['start'] = self._convert_str_time_to_timestamp(params['start'])

        if 'end' in params:
            params['end'] = self._convert_str_time_to_timestamp(params['end'])

        with self.locator.get_service('LogService', metadata) as log_service:
            return self.locator.get_info('LogDataInfo', log_service.list(params))

    @staticmethod
    def _convert_str_time_to_timestamp(str_time):
        date_time = parse(str_time)
        return {
            'seconds': int(time.mktime(date_time.timetuple()))
        }