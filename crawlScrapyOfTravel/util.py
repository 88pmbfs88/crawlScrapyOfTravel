# -*- coding: utf-8 -*-


class SpiderUtil(object):
    @staticmethod
    def listIsEmpty(data):
        """
        如果是空列表会自动生成一个空列表，防止爬去数据超出索引报错

        :param data:
        :return:
        """
        if type(data) == list:
            data = data + ['', '', '']
            return data
        else:
            return data
            raise '传入的值为非列表数据类型！！！'
