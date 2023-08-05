import time
from dateutil.parser import parse
from spaceone.api.monitoring.v1 import metric_pb2, metric_pb2_grpc
from spaceone.core.pygrpc import BaseAPI


class Metric(BaseAPI, metric_pb2_grpc.MetricServicer):

    pb2 = metric_pb2
    pb2_grpc = metric_pb2_grpc

    def list(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service('MetricService', metadata) as metric_service:
            return self.locator.get_info('MetricsInfo', metric_service.list(params))

    def get_data(self, request, context):
        params, metadata = self.parse_request(request, context)

        if 'start' in params:
            params['start'] = self._convert_str_time_to_timestamp(params['start'])

        if 'end' in params:
            params['end'] = self._convert_str_time_to_timestamp(params['end'])

        with self.locator.get_service('MetricService', metadata) as metric_service:
            return self.locator.get_info('MetricDataInfo', metric_service.get_data(params))

    @staticmethod
    def _convert_str_time_to_timestamp(str_time):
        date_time = parse(str_time)
        return {
            'seconds': int(time.mktime(date_time.timetuple()))
        }
