# coding=utf-8
from __future__ import unicode_literals

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from .sakku import Sakku


class Domain(Sakku):
    def __init__(self, api_key, config_path=None, *args, **kwargs):
        super(Domain, self).__init__(api_key=api_key, config_path=config_path, *args, **kwargs)

    def get_all_domains_of_user(self, **kwargs):
        """
         دریافت لیست همه دامنه های کاربر

        :return: list
        """

        return self._request.call("/domain", params=kwargs)

    def get_app_domains(self, app_id, **kwargs):
        """
         دریافت لیست دامنه های یک برنامه

        :param int app_id: شناسه برنامه
        :return: list
        """
        self._validate({"app_id": app_id}, "getAppDomains")
        return self._request.call("/domain/app/{}".format(app_id), params=kwargs)

    def remove_domain(self, app_id, domain, **kwargs):
        """
         حذف دامنه از برنامه

        :param int app_id: شناسه برنامه
        :param str domain: دامنه
        :return: bool
        """

        self._validate({"app_id": app_id, "domain": domain}, "removeDomain")
        return self._request.call("/domain/app/{}?domain={}".format(app_id, domain), params=kwargs, method="delete")

    def add_domain(self, app_id, domain, cert_id=None, **kwargs):
        """
        اضافه کردن دامنه به  برنامه

        :param int app_id: شناسه برنامه
        :param str domain: دامنه
        :param int cert_id: شناسه فایل گواهی
        :return: list
        """
        data = {
            "app_id": app_id,
            "domain": domain
        }

        if cert_id is not None:
            data["certid"] = cert_id

        self._validate(data, "addDomain")
        del data["app_id"]

        return self._request.call("/domain/app/{}/addDomain?{}".format(app_id, urlencode(data)), params=kwargs,
                                  method="post")

    def get_basic_auth_users(self, app_id, **kwargs):
        """
        دریافت احراز هویت پایه کاربران برنامه

        :param int app_id: شناسه برنامه
        :return: list
        """

        self._validate({"app_id": app_id}, "getBasicAuthUsers")
        return self._request.call("/domain/app/{}/basicAuthentication".format(app_id), params=kwargs)

    def add_basic_auth_users(self, app_id, basic_authentication, **kwargs):
        """
        حذف احراز هویت پایه کاربران برنامه

        :param int app_id: شناسه برنامه
        :param list of dict basic_authentication: لیست احراز هویت ها
        :return: list
        """
        self._validate({"app_id": app_id, "basic_authentication": basic_authentication}, "addBasicAuthUsers")
        return self._request.call("/domain/app/{}/basicAuthentication".format(app_id), json=basic_authentication,
                                  params=kwargs,
                                  method="post")

    def delete_basic_auth_users(self, app_id, basic_auth_id, **kwargs):
        """
        حذف احراز هویت پایه کاربران برنامه

        :param int app_id: شناسه برنامه
        :param int basic_auth_id: شناسه برنامه
        :return: list
        """

        self._validate({"app_id": app_id, "basic_auth_id": basic_auth_id}, "deleteBasicAuthUsers")
        return self._request.call("/domain/app/{}/basicAuthentication/{}".format(app_id, basic_auth_id), params=kwargs,
                                  method="delete")

    def get_available_port_options(self, **kwargs):
        """
         دریافت لیست تنظیمات پورت سکو

        :return: list
        """

        return self._request.call("/domain/options", params=kwargs)

    def get_domain_records(self, domain, **kwargs):
        """
        دریافت لیست رکوردهای دامنه کاربر

        :param str domain: دامنه
        :return: list
        """

        data = {"domain": domain}

        self._validate(data, "getDomainRecords")
        return self._request.call("/domain/record?{}".format(urlencode(data)), params=kwargs)

    def add_domain_record(self, domain, record_config, **kwargs):
        """
         اضافه کردن رکورد به دامنه

        :param str domain: دامنه
        :param dict record_config: تنظیمات رکورد
        :return: bool
        """

        self._validate({"domain": domain, "record_config": record_config}, "addDomainRecord")
        return self._request.call("/domain/record?domain={}".format(domain), json=record_config, params=kwargs,
                                  method="post")

    def update_domain_record(self, domain, name, record_type, record_config, **kwargs):
        """
         به‌روز رسانی رکورد دامنه

        :param str domain: دامنه
        :param str name: نام رکورد
        :param str record_type: نوع رکورد
        :param dict record_config: تنظیمات رکورد
        :return: bool
        """
        data = {
            "domain": domain,
            "name": name,
            "record_type": record_type,
            "record_config": record_config,
        }

        self._validate(data, "updateDomainRecord")
        return self._request.call("/domain/record?domain={}&name={}&type={}".format(domain, name, record_type),
                                  json=record_config, params=kwargs, method="put")

    def delete_domain_record(self, domain, name, record_type, **kwargs):
        """
         حذف رکورد دامنه

        :param str domain: دامنه
        :param str name: نام رکورد
        :param str record_type: نوع رکورد
        :return: bool
        """
        data = {
            "domain": domain,
            "name": name,
            "record_type": record_type
        }

        self._validate(data, "deleteDomainRecord")
        data["type"] = data["record_type"]
        del data["record_type"]

        return self._request.call("/domain/record?{}".format(urlencode(data)), params=kwargs, method="delete")
