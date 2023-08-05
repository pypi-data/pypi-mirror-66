# coding=utf-8
from __future__ import unicode_literals
import requests

from .response_handler import ResponseHandler
from .exceptions import HttpException


class RequestHandler(object):

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json"
        }
        self.__last_response = None

    def add_header(self, header, value):
        self.headers[header] = value

    def call(self, url, method="get", params=None, json=None, headers=None, output_as_stream=False,
             **kwargs):
        """

        :param str|unicode url: api address
        :param str|unicode method: http verb - `post`, `get`, `delete`, `put`
        :param dict|None params: dictionary of data
        :param dict|None json: dictionary of body request
        :param dict|None headers: dictionary of headers
        :param bool output_as_stream: output as a stream
        """
        base_url = kwargs.pop("base_url", self.base_url)

        url = base_url + url
        params = self._prepare_params(params)
        headers = self._prepare_headers(headers)
        if kwargs.get("files", None) is not None:
            headers.pop("Content-Type", "")

        try:
            method = method.lower()
            if method == "post":
                self.__last_response = ResponseHandler(requests.post(url, data=params, json=json, headers=headers,
                                                                     **kwargs), stream=output_as_stream)
            elif method == "put":
                self.__last_response = ResponseHandler(requests.put(url, data=params, json=json, headers=headers),
                                                       stream=output_as_stream)
            elif method == "delete":
                self.__last_response = ResponseHandler(requests.delete(url, headers=headers),
                                                       stream=output_as_stream)
            else:
                self.__last_response = ResponseHandler(requests.get(url, params=params, headers=headers),
                                                       stream=output_as_stream)

            return self.__last_response.get_result()
        except requests.exceptions.RequestException as e:
            raise HttpException(e)

    def last_response(self):
        """
        get last response handler

        :return: sakku.response_handler.ResponseHandler
        """
        return self.__last_response

    @staticmethod
    def _prepare_params(params=None):
        if params is None or type(params) is not dict:
            params = {}

        return params

    def _prepare_headers(self, headers=None):
        if headers is not None and type(headers) is dict:
            self.headers.update(headers)

        return self.headers
