# coding=utf-8
from __future__ import unicode_literals


class SakkuException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop("message", "")
        super(SakkuException, self).__init__(*args)

    def __str__(self):
        return self.message


class ConfigException(SakkuException):
    pass


class HttpException(SakkuException):
    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        self.response_handler = kwargs.pop('response_handler', None)
        self.request = kwargs.pop('request', None)
        self.status_code = kwargs.pop('status_code', -1)

        super(HttpException, self).__init__(*args, **kwargs)

    def __str__(self):
        return "{}\nStatus Code : {}".format(self.message, self.status_code)


class InvalidDataException(SakkuException):
    pass
