# coding=utf-8
from __future__ import unicode_literals
from .exceptions import HttpException
import json


class ResponseHandler:
    def __init__(self, response, stream=False):
        self._original_result = {}
        self._result = ""
        self._response = response

        self.__stream = stream
        self.__parse_response()

    def get_result(self):
        return self._result

    def original_result(self):
        """
        get last original result (raw result)

        :return: dict
        """
        return self._original_result

    def __parse_response(self):
        content = self._response.content

        if self.__stream and (200 <= self._response.status_code < 300):
            self._result = self._original_result = content
            return

        if content:
            self._original_result = json.loads(content.decode("utf-8"))
        else:
            self._original_result = {}

        self.__extract_data()

        self.__check_error()

        self._result = self._original_result.get("result", "")

    def __extract_data(self):
        self.__time_stamp = self._original_result.get("timestamp", None)
        self.__path = self._original_result.get("path", None)
        self.__status = self._original_result.get("status", None)
        self.__error = self._original_result.get("error", None)
        self.__message = self._original_result.get("message", None)

    @property
    def time_stamp(self):
        return self.__time_stamp

    @property
    def path(self):
        return self.__path

    @property
    def error(self):
        return self.__error

    @property
    def status(self):
        return self.__status

    @property
    def message(self):
        return self.__message

    def __check_error(self):
        if "error" in self._original_result:
            if not self._original_result["error"]:
                return

            raise HttpException(message=self._original_result.get("message", "error"), response=self._response,
                                response_handler=self, status_code=self._response.status_code)

        message = self._original_result.get("message", self.__get_message(self._response.status_code,
                                                                          "Failed to fetch data"))
        raise HttpException(message=message, response=self._response, response_handler=self,
                            status_code=self._response.status_code)

    @staticmethod
    def __get_message(status_code, default_message):
        messages = {
            400: "Bad request",
            401: "Unauthorized",
            403: "Access denied",
            404: "Not Found",
            405: "Method not allowed",
            406: "Not acceptable",
            500: "Internal server error",
        }

        return messages.get(status_code, default_message)

    def __str__(self):
        return "Error : {}\nMessage : {}\nPath : {}\nStatus : {}\nTimeStamp : {}\n".format(self.__error, self.__message,
                                                                                           self.__path, self.__status,
                                                                                           self.__time_stamp)

    def get_response(self):
        return self._response
