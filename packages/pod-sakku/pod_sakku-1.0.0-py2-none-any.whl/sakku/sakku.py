# coding=utf-8
from __future__ import unicode_literals

from os import path

from jsonschema import validate, ValidationError, SchemaError, Draft7Validator

from .exceptions import InvalidDataException
from .json_schema import JsonSchemaRules
from .request_handler import RequestHandler
from .config import Config
from .response_handler import ResponseHandler


class Sakku(object):
    __slots__ = ("_config", "_request", "__api_key", "__json_schema_rules")

    def __init__(self, api_key, config_path=None, *arg, **kwargs):
        """

        :type str config_path: path to config.ini files
        """
        config_path = config_path or path.join(path.abspath(path.dirname(__file__)), 'config.ini')
        self._config = Config(config_path)
        self._request = RequestHandler(base_url=self._config.get("url", "https://api.sakku.cloud"))
        self.api_key = api_key
        self.__json_schema_rules = JsonSchemaRules(path.join(path.abspath(path.dirname(__file__)), 'json_schema.json'))
        super(Sakku, self).__init__(*arg, **kwargs)

    def last_response(self):  # type: () -> ResponseHandler
        return self._request.last_response()

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, value):
        self.__api_key = value
        self._request.add_header("Authorization", self.__api_key)

    def _validate(self, document, schema_name):
        """
        :raise
            `jsonschema.exceptions.ValidationError` if the instance
                is invalid

            `jsonschema.exceptions.SchemaError` if the schema itself
                is invalid
        """
        try:
            validate(instance=document, schema=self.__json_schema_rules.get_rules(schema_name))
        except ValidationError as e:
            raise InvalidDataException(message="{}: {}".format(".".join([str(elm) for elm in e.path]), e.message),
                                       error_code=887)
        except SchemaError as e:
            raise InvalidDataException(message=e.message, error_code=887)
