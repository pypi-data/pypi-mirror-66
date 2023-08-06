import logging
import sys

from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response

from comk_django_plugin import ALLOW_IP_LIST, COMK_AUTH_CODE, general_resolve_request


class ErrorLogMiddleware(MiddlewareMixin):
    '''
    请求中间件（记录错误信息）

    '''

    def process_exception(self, request, exception):
        '''
        对异常进行记录

        :param request:
        :param exception:
        :return:
        '''
        request_result = general_resolve_request(request)
        log = logging.getLogger('comk_exception_log')  # 加载记录器
        log.exception(request_result)

        remote_addr = request.META.get('REMOTE_ADDR')
        comk_auth_code = request.GET.get('comk_auth_code')

        if hasattr(request,
                   'user') and request.user.is_superuser or remote_addr in ALLOW_IP_LIST or comk_auth_code == COMK_AUTH_CODE:
            # 即使在生产环境下，也允许查看具体的报错信息的方法
            return technical_500_response(request, *sys.exc_info())
