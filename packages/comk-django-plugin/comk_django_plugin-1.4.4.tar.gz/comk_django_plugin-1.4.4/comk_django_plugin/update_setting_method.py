import comk_django_plugin
from comk_django_plugin.logsetting.comk_setting import LOGGING as comk_logsetting
from comk_django_plugin.utils.GeneralMethods import merge_dicts


def auto_update_logsetting(django_logsetting=None):
    '''
    合并日志配置，目的是添加本模块所需要的日志配置

    :param django_logsetting:
    :return:
    '''
    if django_logsetting and isinstance(django_logsetting, dict):
        return merge_dicts(django_logsetting, comk_logsetting)
    else:
        return comk_logsetting


def set_allow_ip_list(allow_ip_list):
    '''
    更改允许查看报错信息的ip

    :param allow_ip_list:
    :return:
    '''
    if isinstance(allow_ip_list, (list, tuple)):
        comk_django_plugin.ALLOW_IP_LIST = allow_ip_list
    else:
        raise Exception('allow_ip_list must be list or tuple')


def set_comk_auth_code(comk_auth_code):
    '''
    更改允许查看报错信息的code

    :param allow_ip_list:
    :return:
    '''
    if isinstance(comk_auth_code, str):
        comk_django_plugin.COMK_AUTH_CODE = comk_auth_code
    else:
        raise Exception('comk_auth_code must be str')


def set_data_len_filter(data_len_filter):
    if isinstance(data_len_filter, bool):
        comk_django_plugin.DATA_LEN_FILTER = data_len_filter
    else:
        raise Exception('data_len_filter must be bool')


def set_data_max_len(data_max_len):
    if isinstance(data_max_len, int):
        comk_django_plugin.DATA_MAX_LEN = data_max_len
    else:
        raise Exception('data_max_len must be int')


def set_res_timeout_filter(set_res_timeout_filter):
    if isinstance(set_res_timeout_filter, bool):
        comk_django_plugin.RES_TIMEOUT_FILTER = set_res_timeout_filter
    else:
        raise Exception('set_res_timeout_filter must be bool')


def set_res_timeout_value(res_timeout_value):
    if isinstance(res_timeout_value, int):
        comk_django_plugin.RES_TIMEOUT_VALUE = res_timeout_value
    else:
        raise Exception('res_timeout_value must be int')
