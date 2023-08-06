from .utils.GeneralMethods import general_resolve_request_data, general_resolve_request, general_resolve_response
from .utils.BaseMoudel import BaseMoudel
from .utils.PublicServer import PublicServer
from .utils.PublicDao import PublicDao
from .update_setting_method import *

# 可以DEBUG查看500错误的限制
ALLOW_IP_LIST = []
COMK_AUTH_CODE = 'COMK_AUTH_CODE'

# 数据过滤
DATA_LEN_FILTER = True
DATA_MAX_LEN = 1000

# 超时异常记录设置
RES_TIMEOUT_FILTER = True
RES_TIMEOUT_VALUE = 5
