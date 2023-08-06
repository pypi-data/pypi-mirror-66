import datetime
import logging

from django.utils.deprecation import MiddlewareMixin

from comk_django_plugin import general_resolve_request, general_resolve_response, DATA_LEN_FILTER, DATA_MAX_LEN, \
    RES_TIMEOUT_FILTER, RES_TIMEOUT_VALUE


class RequestLogMiddleware(MiddlewareMixin):
    '''
    请求中间件（记录请求、返回与错误信息）

    '''

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.start_time = None  # 程序开始运行时间
        self.end_time = None  # 程序结束运行时间

    def process_request(self, request):
        self.start_time = datetime.datetime.now()  # 程序开始运行时间
        return None

    def process_response(self, request, response):
        '''
        对返回进行记录

        :param request:
        :param response:
        :return:
        '''
        request_result = general_resolve_request(request, DATA_LEN_FILTER, DATA_MAX_LEN)
        response_result = general_resolve_response(response, DATA_LEN_FILTER, DATA_MAX_LEN)

        self.end_time = datetime.datetime.now()  # 程序结束运行时间
        run_time = (self.end_time - self.start_time).total_seconds()
        log = logging.getLogger('comk_request_log')  # 加载记录器
        process_msg = '{} -- {} -- {}'.format(request_result, response_result, str(run_time))
        log.info(process_msg)

        # 超时记录
        if RES_TIMEOUT_FILTER and int(run_time) >= RES_TIMEOUT_VALUE:
            log = logging.getLogger('comk_long_response_time_log')  # 加载记录器
            time_out_msg = '{} -- {}'.format(process_msg, '设置超时时间:{}s'.format(RES_TIMEOUT_VALUE))
            log.info(time_out_msg)

        return response
