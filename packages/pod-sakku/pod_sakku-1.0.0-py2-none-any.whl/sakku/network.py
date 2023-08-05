# coding=utf-8
from __future__ import unicode_literals

from .sakku import Sakku


class Network(Sakku):
    def __init__(self, api_key, config_path=None, *args, **kwargs):
        super(Network, self).__init__(api_key=api_key, config_path=config_path, *args, **kwargs)

    def get_networks(self, **kwargs):
        """
         دریافت لیست شبکه ها

        :return: list
        """
        return self._request.call("/app/network", params=kwargs)

    def create_network(self, name, **kwargs):
        """
        ایجاد شبکه

        :param str name: نام شبکه
        :return: dict
        """

        self._validate({"name": name}, "createNetwork")
        return self._request.call("/app/network/create?name={}".format(name), params=kwargs, method="post")

    def add_app_to_network(self, app_id, name, **kwargs):
        """
        اضافه کردن برنامه به شبکه

        :param int app_id: شناسه برنامه
        :param str name: نام شبکه
        :return: bool
        """
        self._validate({"app_id": app_id, "name": name}, "addAppToNetwork")
        result = self._request.call("/app/network/{}/addApp?appId={}".format(name, app_id), params=kwargs,
                                    method="post")

        if result is None:
            return True

        return result

    def remove_app_from_network(self, app_id, name, **kwargs):
        """
         حذف برنامه از شبکه

        :param int app_id: شناسه برنامه
        :param str name: نام شبکه
        :return: bool
        """
        self._validate({"name": name, "app_id": app_id}, "removeAppFromNetwork")
        result = self._request.call("/app/network/{}/removeApp?appId={}".format(name, app_id), params=kwargs,
                                    method="post")

        if result is None:
            return True

        return result

    def delete_network_by_user(self, name, force=False, **kwargs):
        """
         حذف شبکه به وسیله کاربر

        :param str name: نام شبکه
        :param bool force: آیا در هر صورتی حذف شود؟
        :return: bool
        """

        self._validate({"name": name, "force": force}, "deleteNetworkByUser")
        result = self._request.call("/app/network/{}?force={}".format(name, str(force).lower()), params=kwargs,
                                    method="delete")

        if result is None:
            return True

        return result
