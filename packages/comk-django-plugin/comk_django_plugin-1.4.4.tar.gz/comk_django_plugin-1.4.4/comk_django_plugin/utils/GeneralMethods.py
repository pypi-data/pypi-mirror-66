import json

from django.http import JsonResponse


def general_resolve_request_data(request):
    '''
    解析 request 的请求数据为 dict

    :param request:
    :return:
    '''
    request_data = dict()
    try:
        request_data.update(json.loads(request.body))
    except:
        pass
    request_data.update(request.GET.dict())
    request_data.update(request.POST.dict())
    return request_data


def general_resolve_request(request, data_len_filter=False, data_max_len=0):
    '''
    解析 request 的所有参数为 str

    :param request:
    :return:
    '''
    return_L = []
    return_L.append(request.META.get('REMOTE_ADDR'))
    return_L.append(request.scheme)
    return_L.append(request.get_host())
    return_L.append(request.path)
    return_L.append(request.method)

    if hasattr(request, 'user') and request.user.is_authenticated():
        user_key = str(request.user.username)
    else:
        user_key = 'AnonymousUser'
    return_L.append(user_key)

    # 返回请求数据
    req_data = str(general_resolve_request_data(request))
    # 请求数据过滤
    if req_data and data_len_filter and len(req_data) >= data_max_len:
        req_data = '请求数据过长，在此忽略'

    return_L.append(req_data)
    return ' -- '.join(return_L)


def general_resolve_response_data(response):
    '''
    解析 response 的返回数据为 dict

    :param request:
    :return:
    '''
    data = {}
    status_code = str(response.status_code)
    if status_code.startswith('2'):
        if isinstance(response, JsonResponse):
            data = json.loads(response.content)
        # elif isinstance(response, HttpResponse):
        #     data = response.content.decode('utf-8')
    return data


def general_resolve_response(response, data_len_filter=False, data_max_len=0):
    '''
    解析 response 的所有参数为 str

    :param response:
    :return:
    '''
    return_L = []

    status_code = str(response.status_code)
    return_L.append(status_code)

    # 获取返回数据
    resp_data = str(general_resolve_response_data(response))

    # 返回数据过滤
    if resp_data and data_len_filter and len(resp_data) >= data_max_len:
        resp_data = '返回数据过长，在此忽略'

    return_L.append(resp_data)
    return ' -- '.join(return_L)


def merge_dicts(dict_one: dict, dict_two: dict):
    '''
    深度合并两个dict

    :param dict_one:
    :param dict_two:
    :return:
    '''
    one_keys = dict_one.keys()
    tow_keys = dict_two.keys()
    for tow_key in tow_keys:
        if tow_key in one_keys:
            one_value = dict_one.get(tow_key)
            two_value = dict_two.get(tow_key)
            if isinstance(one_value, dict) and isinstance(two_value, dict):
                merge_dicts(one_value, two_value)
        else:
            dict_one[tow_key] = dict_two.get(tow_key)
    return dict_one
