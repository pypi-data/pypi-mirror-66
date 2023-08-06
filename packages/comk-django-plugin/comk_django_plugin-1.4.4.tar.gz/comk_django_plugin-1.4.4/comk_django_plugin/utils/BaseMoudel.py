import datetime


class BaseMoudel():
    '''
    服务以及业务的模型基类

    '''

    def __init__(self):
        self.response_data = {'code': '8999', 'response_data': '', 'msg': '', 'timestamp': ''}

    def __build_return_response_data(self, code, msg=None, response_data=None, timestamp_now=True):
        '''
        构造返回信息

        :param code:
        :param msg:
        :return:
        '''
        self.response_data['code'] = code
        if msg:
            self.response_data['msg'] = msg
        if response_data:
            self.response_data['response_data'] = response_data
        if timestamp_now:
            self.response_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.response_data

    def build_return_response_data(self, code, msg=None, response_data=None, timestamp_now=True):
        '''
        构造返回信息

        :param code:
        :param msg:
        :return:
        '''
        print('the method build_return_response_data will not support in next version, '
              'please use build_success_response_data or build_error_response_data')
        return self.__build_return_response_data(code, msg, response_data, timestamp_now)

    def build_success_response_data(self, response_data=None, timestamp_now=True):
        '''
        构建业务成功的返回数据

        :param response_data:
        :return:
        '''

        return self.__build_return_response_data('1000', response_data=response_data, timestamp_now=timestamp_now)

    def build_error_response_data(self, code='1000', msg=None, timestamp_now=True):
        '''
        构建业务失败的返回数据

        :param msg:
        :return:
        '''

        return self.__build_return_response_data(code, msg=msg, timestamp_now=timestamp_now)
