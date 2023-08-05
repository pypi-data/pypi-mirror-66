# coding=utf-8
from __future__ import unicode_literals
from .sakku import Sakku


class Catalog(Sakku):
    def __init__(self, api_key, config_path=None, *args, **kwargs):
        super(Catalog, self).__init__(api_key=api_key, config_path=config_path, *args, **kwargs)

    def get_all_catalogs(self, **kwargs):
        """
        دریافت لیست دسته های کاتالوگ ها

        :return: list
        """

        self._validate(kwargs, "getAllCatalogs")
        return self._request.call("/catalog", params=kwargs)

    def create_catalog_app(self, catalog_id, catalog_app_config, **kwargs):
        """
        ایجاد کاتالوگ جدید

        :param int catalog_id: شناسه دسته بندی کاتالوگ
        :param dict catalog_app_config: تنظیمات کاتالوگی که ایجاد خواهد شد
        :return: dict
        """
        self._validate({"catalog_id": catalog_id, "catalog_app_config": catalog_app_config}, "createCatalogApp")

        return self._request.call("/catalog/{}/create".format(catalog_id), json=catalog_app_config, params=kwargs,
                                  method="post")

    def update_catalog(self, catalog_app_id, catalog_app_config, **kwargs):
        """
        ویرایش کاتالوگ

        :param int catalog_app_id:
        :param dict catalog_app_config: تنظیمات
        :return: dict
        """

        self._validate({"catalog_app_id": catalog_app_id, "catalog_app_config": catalog_app_config}, "updateCatalog")

        return self._request.call("/catalog/{}/update".format(catalog_app_id), json=catalog_app_config, params=kwargs,
                                  method="put")

    def get_catalog_app(self, catalog_id, catalog_app_id, **kwargs):
        """
        دریافت اطلاعات کاتالوگ با شناسه کاتالوگ و شناسه دسته کاتالوگ

        :param int catalog_id: شناسه کاتالوگ
        :param int catalog_app_id: شناسه دسته کاتالوگ
        :return: dict
        """

        self._validate({"catalog_id": catalog_id, "catalog_app_id": catalog_app_id}, "getCatalogApp")
        return self._request.call("/catalog/{}/{}".format(catalog_id, catalog_app_id), params=kwargs)

    def create_catalog_app_by_sakku_app(self, app_id, catalog_id, catalog_app_config, **kwargs):
        """
        ایجاد کاتالوگ جدید به وسیله برنامه موجود

        :param int app_id: شناسه برنامه
        :param int catalog_id: شناسه دسته بندی کاتالوگ
        :param dict catalog_app_config: تنظیمات کاتالوگی که ایجاد خواهد شد
        :return: dict
        """
        self._validate({"app_id": app_id, "catalog_id": catalog_id, "catalog_app_config": catalog_app_config},
                       "createCatalogAppBySakkuApp")
        return self._request.call("/catalog/{}/create/fromApplication?appId={}".format(catalog_id, app_id),
                                  json=catalog_app_config, method="post")

    def get_all_catalog_app_by_id(self, catalog_id, **kwargs):
        """
        دریافت کاتالوگ های یک دسته بندی با شناسه دسته کاتالوگ ها

        :param int catalog_id: شناسه دسته بندی کاتالوگ
        :return: list
        """
        self._validate({"catalog_id": catalog_id}, "getAllCatalogAppById")
        return self._request.call("/catalog/{}".format(catalog_id), params=kwargs)

    def get_user_feedback_catalog(self, status=False, **kwargs):
        """
        دریافت لیست بازخورد کاربران برای کاتالوگ

        :param bool status: آیا توسط ادمین بررسی شده است یا خیر؟
        :return: list
        """
        self._validate({"status": status}, "getUserFeedbackCatalog")
        return self._request.call("/catalog/feedback?status=".format(str(status).lower()), params=kwargs)

    def add_user_feedback_catalogs(self, subject, description, feedback_type, **kwargs):
        """
        اضافه کردن بازخورد کاربر به کاتالوگ

        :param str subject: عنوان
        :param str description: توضیحات
        :param str feedback_type: نوع بازخورد
        :return: bool
        """
        data = kwargs.copy()
        data["subject"] = subject
        data["description"] = description
        data["feedback_type"] = feedback_type

        self._validate(data, "addUserFeedbackCatalogs")
        data["type"] = feedback_type
        del data["feedback_type"]

        return self._request.call("/catalog/feedback", json=data, method="post")

    def get_all_meta_data(self, page=1, size=50, **kwargs):
        """
        دریافت لیست تمامی متادیتا

        :param int page: شماره صفحه
        :param int size: تعداد در هر صفحه
        :return: list
        """

        self._validate({"page": page, "size": size}, "getAllMetaData")
        return self._request.call("/catalog/metadata?page={}&size={}".format(page, size), params=kwargs)

    def validate_meta_data(self, meta_data, **kwargs):
        """
        اعتبارسنجی متادیتا

        :param dict meta_data: اطلاعات متادیتایی که باید اعتبار سنجی شود
        :return: dict
        """
        self._validate({"meta_data": meta_data}, "validateMetaData")
        return self._request.call("/catalog/metadata/validate", json=meta_data, params=kwargs, method="post")

    def deploy_app_from_catalog(self, catalog_app_id, settings, files=None, **kwargs):
        """
        ایجاد برنامه از طریق کاتالوگ

        :param int catalog_app_id: شناسه کاتالوگ
        :param dict settings: اطلاعات برنامه
        :param list files: اطلاعات برنامه
        :return: list
        """
        return self.__deploy_app_from_catalog(catalog_app_id=catalog_app_id, settings=settings, files=files, test=False,
                                              **kwargs)

    def deploy_app_from_catalog_test(self, catalog_app_id, settings, files=None, **kwargs):
        """
        مشاهده کاتالوگ یک دسته با شناسه ( متد تستی )

        :param int catalog_app_id: شناسه کاتالوگ
        :param dict settings: اطلاعات برنامه
        :param list files: اطلاعات برنامه
        :return: list
        """
        return self.__deploy_app_from_catalog(catalog_app_id=catalog_app_id, settings=settings, files=files, test=True,
                                              **kwargs)

    def __deploy_app_from_catalog(self, catalog_app_id, settings, files=None, test=False, **kwargs):
        """
        ایجاد برنامه از طریق کاتالوگ

        :param int catalog_app_id: شناسه کاتالوگ
        :param dict settings: اطلاعات برنامه
        :param list files: اطلاعات برنامه
        :param bool test: سرویس تستی اجرا شود؟
        :return: list
        """
        data = kwargs.copy()
        data["catalog_app_id"] = catalog_app_id
        data["settings"] = settings

        if files is not None:
            data["files"] = files

        self._validate(data, "deployAppFromCatalog")
        del data["catalog_app_id"]

        if test:
            url = "/test"
        else:
            url = ""

        return self._request.call("/catalog/deploy/{}{}".format(catalog_app_id, url), params=data, method="post")

