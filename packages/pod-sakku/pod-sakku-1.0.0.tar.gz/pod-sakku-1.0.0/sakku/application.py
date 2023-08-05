# coding=utf-8
from __future__ import unicode_literals

from .sakku import Sakku
from .exceptions import InvalidDataException
from os import path


class Application(Sakku):
    def __init__(self, api_key, config_path=None, *args, **kwargs):
        super(Application, self).__init__(api_key=api_key, config_path=config_path, *args, **kwargs)

    def get_user_apps_list(self, **kwargs):
        """
         دریافت لیست برنامه های کاربر

        :return: list
        """
        kwargs.setdefault("page", 1)
        kwargs.setdefault("size", 10)
        self._validate(kwargs, "getUserAppsList")
        return self._request.call("/app", params=kwargs)

    def create_app(self, config, **kwargs):
        """
        ایجاد یک برنامه جدید

        :param dict config: تنظیمات برنامه
        :return: dict
        """

        self._validate(self.__delete_empty_item(config.copy()), "createApp")
        return self._request.call("/app", params=kwargs, json=config, method="post")

    def delete_app_by_id(self, app_id, force=False):
        """
        حذف یک برنامه

        :param int app_id: شناسه برنامه
        :param bool force: آیا برنامه در هر صورتی حذف شود؟
        :return: str
        """
        self._validate({"app_id": app_id, "force": force}, "deleteAppById")

        return self._request.call("/app/{}?force={}".format(app_id, str(force).lower()), method="delete")

    def commit_app_container(self, app_id, container_id=None, tag=None, **kwargs):
        """
        کامیت کانتینر برنامه

        :param int app_id: شناسه برنامه
        :param str container_id: 	شناسه کانتینر	به صورت پیش فرض آخرین شناسه کانتینر استفاده می شود
        :param str tag: تگ - به صورت پیشفرض به صورت `yyyy-MM-dd-HH-mm-ss` اعمال می شود
        :return: str
        """
        if container_id is not None:
            kwargs["containerId"] = container_id

        if tag is not None:
            kwargs["tag"] = tag
        data = kwargs.copy()
        data["app_id"] = app_id
        self._validate(data, "commitAppContainer")
        return self._request.call("/app/{}/commit".format(app_id), params=kwargs)

    def update_app_config(self, app_id, config, **kwargs):
        """
        به روزرسانی تنظیمات برنامه

        :param int app_id: شناسه برنامه
        :param dict config: تنظیمات برنامه

        :return: dict
        """
        self._validate({"app_id": app_id, "config": config}, "updateAppConfig")
        return self._request.call("/app/{}/config".format(app_id), params=kwargs, json=config, method="put")

    def get_real_time_deploy(self, app_id, **kwargs):
        """
        دریافت وضعیت استقرار بلادرنگ برنامه

        :param int app_id: شناسه برنامه

        :return: dict
        """
        self._validate({"app_id": app_id}, "getRealTimeDeploy")
        return self._request.call("/app/{}/deploy/state".format(app_id), params=kwargs)

    def get_fake_app_state(self, app_id, **kwargs):
        """
        دریافت وضعیت برنامه (برای تست)

        :param int app_id: شناسه برنامه

        :return: dict
        """
        self._validate({"app_id": app_id}, "getFakeAppState")
        return self._request.call("/app/{}/deploy/state".format(app_id), params=kwargs)

    def logs_export(self, app_id, from_date=None, to_date=None, save_to=None, **kwargs):
        """
        دریافت لاگ های برنامه

        :param int app_id: شناسه برنامه
        :param int|None from_date: تایم استمپ شروع به صورت یک عدد ۱۳ رقمی
        :param int|None to_date: تایم استمپ پایان به صورت یک عدد ۱۳ رقمی
            در صورتی که ارسال نشود،زمان جاری درنظر گرفته می شود
        :param str|None save_to: آدرس محل ذخیره سازی
            در صورتی که آدرس وارد شود، خروجی در آدرس فایل داده شده ذخیره می شود

        :return: str
        """

        if from_date is not None:
            kwargs["fromDate"] = from_date

        if to_date is not None:
            kwargs["toDate"] = to_date

        kwargs["token"] = self.api_key

        data = kwargs.copy()
        data["app_id"] = app_id
        self._validate(data, "logsExport")
        content = self._request.call("/app/{}/logs/export".format(app_id), params=kwargs, output_as_stream=True)
        content = content.decode("utf-8")

        if save_to is None:
            return content

        self.__write_to_file(save_to, content)

    @staticmethod
    def __write_to_file(path_of_file, content):
        with open(path_of_file, "w") as file_handler:
            file_handler.write(content)

    def get_app_owner(self, app_id, **kwargs):
        """
        دریافت اطلاعات مالک برنامه

        :param int app_id: شناسه برنامه

        :return: dict
        """
        self._validate({"app_id": app_id}, "getAppOwner")
        return self._request.call("/app/{}/owner".format(app_id), params=kwargs)

    def rebuild_app(self, app_id, **kwargs):
        """
        بازسازی سورس برنامه

        :param int app_id: شناسه برنامه

        :return: str
        """
        self._validate({"app_id": app_id}, "rebuildApp")
        return self._request.call("/app/{}/rebuild".format(app_id), params=kwargs)

    def restart_app_by_id(self, app_id, **kwargs):
        """
        راه اندازی مجدد برنامه

        :param int app_id: شناسه برنامه

        :return: bool
        """
        data = kwargs.copy()
        data["app_id"] = app_id

        self._validate(self.__delete_empty_item(data), "restartAppById")
        return self._request.call("/app/{}/restart".format(app_id), params=kwargs)

    def get_app_setting(self, app_id, **kwargs):
        """
        دریافت تنظیمات برنامه

        :param int app_id: شناسه برنامه

        :return: dict
        """
        self._validate({"app_id": app_id}, "getAppSetting")
        return self._request.call("/app/{}/setting".format(app_id), params=kwargs)

    def start_app_by_id(self, app_id, **kwargs):
        """
        شروع برنامه

        :param int app_id: شناسه برنامه

        :return: str
        """
        if kwargs.get("tag", ""):
            kwargs["committed"] = True
        data = kwargs.copy()
        data["app_id"] = app_id
        self._validate(self.__delete_empty_item(data), "startAppById")
        return self._request.call("/app/{}/start".format(app_id), params=kwargs)

    def stop_app_by_id(self, app_id, **kwargs):
        """
        توقف برنامه

        :param int app_id: شناسه برنامه

        :return: str
        """
        data = kwargs.copy()
        data["app_id"] = app_id
        self._validate(self.__delete_empty_item(data), "stopAppById")
        return self._request.call("/app/{}/stop".format(app_id), params=kwargs)

    def stop_app_deploy(self, app_id, **kwargs):
        """
        توقف عملیات بارگذاری

        :param int app_id: شناسه برنامه

        :return: str
        """
        self._validate({"app_id": app_id}, "stopAppDeploy")
        return self._request.call("/app/{}/stopDeploying".format(app_id), params=kwargs)

    def get_app_versions(self, app_id, **kwargs):
        """
         لیست نسخه های برنامه

        :param int app_id: شناسه برنامه

        :return: list
        """
        self._validate({"app_id": app_id}, "getAppVersions")
        return self._request.call("/app/{}/versions".format(app_id), params=kwargs)

    def create_app_web_hooks(self, app_id, config, **kwargs):
        """
        ایجاد وب هوک برای برنامه

        :param int app_id: شناسه برنامه
        :param dict config: تنظیمات وب هوک

        :return: dict
        """
        config["applicationId"] = app_id

        self._validate({"app_id": app_id, "config": config}, "createAppWebHooks")
        return self._request.call("/app/{}/webhooks".format(app_id), params=kwargs, json=config, method="post")

    def get_app_by_id(self, app_id, **kwargs):
        """
        دریافت اطلاعات برنامه

        :param int app_id: شناسه برنامه

        :return: dict
        """
        self._validate({"app_id": app_id}, "getAppById")
        return self._request.call("/app/{}".format(app_id), params=kwargs)

    def get_app_activity(self, app_id, page=1, size=50, **kwargs):
        """
        دریافت فعالیت های بر روی برنامه

        :param int app_id: شناسه برنامه
        :param int page: شماره صفحه
        :param int size: تعداد آیتم در هر صفحه

        :return: list
        """
        kwargs["size"] = size
        kwargs["page"] = page
        data = kwargs.copy()
        data["app_id"] = app_id
        self._validate(self.__delete_empty_item(data), "getAppActivity")
        return self._request.call("/app/{}/activity".format(app_id), params=kwargs)

    def get_chat_data(self, app_id, **kwargs):
        """
        دریافت اطلاعات گفتگوهای هر برنامه

        :param int app_id: شناسه برنامه

        :return: dict
        """
        self._validate({"app_id": app_id}, "getChatData")
        return self._request.call("/app/{}/chat".format(app_id), params=kwargs)

    def check_app_health(self, app_id, **kwargs):
        """
        بررسی سلامت برنامه

        :param int app_id: شناسه برنامه

        :return: list
        """
        self._validate({"app_id": app_id}, "checkAppHealth")
        return self._request.call("/app/{}/check".format(app_id), params=kwargs)

    def check_app_health_by_id(self, app_id, health_id, **kwargs):
        """
        بررسی سلامت برنامه براساس شناسه سرویس سلامت

        :param int app_id: شناسه برنامه
        :param int health_id: شناسه لاگ

        :return: dict
        """
        self._validate({"app_id": app_id, "health_id": health_id}, "checkAppHealthById")
        return self._request.call("/app/{}/check/{}".format(app_id, health_id), params=kwargs)

    def get_app_collaborators(self, app_id, page=1, size=50, all_collaborators=False, **kwargs):
        """
        مشاهده دسترسی های برنامه

        :param int app_id: شناسه برنامه
        :param int page: شماره صفحه
        :param int size: تعداد خروجی در هر صفحه
        :param bool all_collaborators: همکاران حذف شده هم برگردانده شود؟

        :return: list
        """
        kwargs["page"] = page
        kwargs["size"] = size
        kwargs["all"] = all_collaborators
        data = kwargs.copy()
        data["app_id"] = app_id
        data["all_collaborators"] = data.pop("all")
        self._validate(data, "getAppCollaborators")
        return self._request.call("/app/{}/collaborators".format(app_id), params=kwargs)

    def add_app_collaborator(self, app_id, email, access_level, image_registry_access, level=7, **kwargs):
        """
        افزودن دسترسی به برنامه

        :param int app_id: شناسه برنامه
        :param str email: ایمیل کاربر
        :param str access_level: سطح دسترسی فرد به برنامه
        :param str image_registry_access: سطح دسترسی فرد به image برنامه
        :param int level: سطح ارسال پیامک و ایمیل مربوط به این برنامه برای کاربر اضافه‌شده

        :return: dict
        """
        data = {
            "accessLevel": access_level,
            "email": email,
            "imageRegistry": image_registry_access
        }
        data_validation = data.copy()
        data_validation["app_id"] = app_id
        self._validate(data_validation, "addAppCollaborator")
        return self._request.call("/app/{}/collaborators?level={}".format(app_id, level), params=kwargs, json=data,
                                  method="post")

    def update_app_collaborator(self, app_id, collaborator_id, email, access_level, image_registry_access, level=7,
                                **kwargs):
        """
        تغییر سطح دسترسی کاربر به برنامه

        :param int app_id: شناسه برنامه
        :param int collaborator_id: شناسه دسترسی فرد به برنامه
        :param str email: ایمیل کاربر
        :param str access_level: سطح دسترسی فرد به برنامه
        :param str image_registry_access: سطح دسترسی فرد به image برنامه
        :param int level: سطح ارسال پیامک و ایمیل مربوط به این برنامه برای کاربر اضافه‌شده

        :return: dict
        """
        data = {
            "accessLevel": access_level,
            "email": email,
            "imageRegistry": image_registry_access
        }

        data_validation = data.copy()
        data_validation["app_id"] = app_id
        data_validation["collaborator_id"] = collaborator_id
        self._validate(data_validation, "updateAppCollaborator")
        return self._request.call("/app/{}/collaborators/{}?level={}".format(app_id, collaborator_id, level), json=data,
                                  params=kwargs, method="post")

    def delete_app_collaborator(self, app_id, collaborator_id, **kwargs):
        """
        حذف دسترسی یک فرد به برنامه

        :param int app_id: شناسه برنامه
        :param int collaborator_id: شناسه دسترسی فرد به برنامه

        :return: str
        """
        self._validate({"app_id": app_id, "collaborator_id": collaborator_id}, "deleteAppCollaborator")
        return self._request.call("/app/{}/collaborators/{}".format(app_id, collaborator_id), method="delete",
                                  params=kwargs)

    def verify_user_command_permission(self, app_id, cmd, **kwargs):
        """
        دسترسی اجرای دستور
        با استفاده از این متد می‌توانید بررسی کنید که می‌توانید یک دستور را روی برنامه اعمال کنید یا خیر.


        :param int app_id: شناسه برنامه
        :param str cmd: دستور

        :return: bool
        """
        kwargs["cmd"] = cmd
        data = kwargs.copy()
        data["app_id"] = app_id
        self._validate(self.__delete_empty_item(data), "verifyUserCommandPermission")
        return self._request.call("/app/{}/exec/verify".format(app_id), params=kwargs)

    def get_app_health_check(self, app_id, **kwargs):
        """
        مشاهده تنظیمات ثبت شده برای بررسی سلامت برنامه

        :param int app_id: شناسه برنامه

        :return: list
        """
        self._validate({"app_id": app_id}, "getAppHealthCheck")
        return self._request.call("/app/{}/healthCheck".format(app_id), params=kwargs)

    def add_app_health_check(self, app_id, end_point="/ping", check_rate=0, schema="https", initial_delay=0,
                             response_code=200, response_string="Ok.", **kwargs):
        """
        تنظیم آدرس برای بررسی سلامت برنامه

        :param int app_id: شناسه برنامه
        :param str end_point: آدرس سرویس
        :param int check_rate: بررسی سلامت برنامه هر چند میلی ثانیه یک بار انجام شود.
        :param str schema: نوع پروتکل - `http` یا `https`
        :param int initial_delay: شناسه برنامه
        :param int response_code: کد صحیحی که برنامه باید در جواب درخواست ارسال‌شده بدهد.
        :param str response_string: پاسخ صحیحی که برنامه باید در جواب درخواست ارسال‌شده بدهد.

        :return: list
        """

        data = {
            "checkRate": check_rate,
            "endpoint": end_point,
            "initialDelay": initial_delay,
            "responseCode": response_code,
            "responseString": response_string,
            "schema": schema
        }
        data_validation = data.copy()
        data_validation["app_id"] = app_id
        self._validate(self.__delete_empty_item(data_validation), "addAppHealthCheck")
        return self._request.call("/app/{}/healthCheck".format(app_id), params=kwargs, json=data, method="post")

    def delete_all_app_health_checks(self, app_id, path, **kwargs):
        """
        حذف تمام آدرس های بررسی سلامت برنامه براساس آدرس

        :param int app_id: شناسه برنامه
        :param str path: آدرس سرویس سلامت

        :return: list
        """
        self._validate({"app_id": app_id, "path": path}, "deleteAllAppHealthChecks")
        return self._request.call("/app/{}/healthCheck?path={}".format(app_id, path), params=kwargs, method="delete")

    def update_health_check_by_id(self, app_id, health_id, end_point="/ping", check_rate=0, schema="https",
                                  initial_delay=0, response_code=200, response_string="Ok.", **kwargs):
        """
        ویرایش تنظیمات ثبت شده برای بررسی سلامت برنامه

        :param int app_id: شناسه برنامه
        :param int health_id: شناسه سرویس بررسی سلامت برنامه
        :param str end_point: آدرس سرویس
        :param int check_rate: بررسی سلامت برنامه هر چند میلی ثانیه یک بار انجام شود.
        :param str schema: نوع پروتکل - `http` یا `https`
        :param int initial_delay: شناسه برنامه
        :param int response_code: کد صحیحی که برنامه باید در جواب درخواست ارسال‌شده بدهد.
        :param str response_string: پاسخ صحیحی که برنامه باید در جواب درخواست ارسال‌شده بدهد.

        :return: dict
        """
        data = {
            "checkRate": check_rate,
            "endpoint": end_point,
            "initialDelay": initial_delay,
            "responseCode": response_code,
            "responseString": response_string,
            "schema": schema
        }

        data_validation = data.copy()
        data_validation["app_id"] = app_id
        data_validation["health_id"] = health_id
        self._validate(self.__delete_empty_item(data_validation), "updateHealthCheckById")
        return self._request.call("/app/{}/healthCheck/{}".format(app_id, health_id), json=data, params=kwargs,
                                  method="put")

    def delete_health_check_by_id(self, app_id, health_id, **kwargs):
        """
        حذف تست سلامت برنامه با شناسه

        :param int app_id: شناسه برنامه
        :param int health_id: شناسه سرویس بررسی سلامت برنامه

        :return: dict
        """
        self._validate({"app_id": app_id, "health_id": health_id}, "deleteHealthCheckById")
        return self._request.call("/app/{}/healthCheck/{}".format(app_id, health_id), params=kwargs, method="delete")

    def get_real_time_app_logs_by_id(self, app_id, time, **kwargs):
        """
        دریافت لاگ بلادرنگ برنامه

        :param int app_id: شناسه برنامه
        :param int time: تایم استمپ آخرین زمان لاگ به صورت ۱۳ رقمی

        :return: dict
        """
        kwargs["time"] = time
        self._validate({"app_id": app_id, "time": time}, "getRealTimeAppLogsById")
        return self._request.call("/app/{}/logs".format(app_id), params=kwargs)

    def transfer_app_by_id(self, app_id, customer_email, add_as_collaborator=False, transfer_git=False,
                           transfer_image_repo=False, **kwargs):
        """
        انتقال برنامه با شناسه

        :param int app_id: شناسه برنامه
        :param str customer_email: ایمیل فردی که می‌خواهید برنامه را به او منتقل کنید
        :param bool add_as_collaborator: آیا صاحب برنامه بعد از انتقال آن، با سطح دسترسی VIEW به برنامه
        دسترسی داشته‌باشد یا خیر.
        :param bool transfer_git: آیا ریپازیتوری گیت برنامه منتقل شود یا خیر
        :param bool transfer_image_repo: image برنامه منتقل شود یا خیر

        :return: bool
        """
        data = {
            "customerEmail": customer_email,
            "transferGit": transfer_git,
            "transferImageRepo": transfer_image_repo,
            "addAsCollaborator": add_as_collaborator
        }
        data_validation = data.copy()
        data_validation["app_id"] = app_id
        self._validate(self.__delete_empty_item(data_validation), "transferAppById")
        return self._request.call("/app/{}/transfer".format(app_id), params=kwargs, json=data, method="post")

    def get_app_web_hooks(self, app_id, **kwargs):
        """
        دریافت وب هوک های برنامه

        :param int app_id: شناسه برنامه

        :return: list
        """
        self._validate({"app_id": app_id}, "getAppWebHooks")
        return self._request.call("/app/{}/webhooks".format(app_id), params=kwargs)

    def update_app_web_hook_by_id(self, app_id, web_hook_id, config, **kwargs):
        """
        به روز رسانی هوک برنامه

        :param int app_id: شناسه برنامه
        :param int web_hook_id: شناسه وب هوک
        :param dict config: اطلاعات وب هوک

        :return: dict
        """
        config["applicationId"] = app_id
        self._validate({"app_id": app_id, "web_hook_id": web_hook_id, "config": config}, "updateAppWebHookById")
        return self._request.call("/app/{}/webhooks/{}".format(app_id, web_hook_id), params=kwargs, json=config,
                                  method="post")

    def delete_app_web_hook_by_id(self, app_id, web_hook_id, **kwargs):
        """
        حذف وب هوک

        :param int app_id: شناسه برنامه
        :param int web_hook_id: شناسه وب هوک

        :return: int
        """
        self._validate({"app_id": app_id, "web_hook_id": web_hook_id}, "deleteAppWebHookById")
        return self._request.call("/app/{}/webhooks/{}".format(app_id, web_hook_id), params=kwargs, method="delete")

    def get_app_by_name(self, name, **kwargs):
        """
        دریافت برنامه از طریق نام برنامه

        :param str name: نام برنامه

        :return: dict
        """
        self._validate({"name": name}, "getAppByName")
        return self._request.call("/app/byName/{}".format(name), params=kwargs)

    def create_app_by_docker_compose(self, compose_path, global_config, **kwargs):
        """
        ایجاد برنامه با Docker Compose

        :param str compose_path: مسیر فایل docker-compose
        :param dict global_config:

        :return: list
        """

        self.__check_exist_file(compose_path)

        files = {
            'composeFile': ('docker-compose.yml', open(compose_path, 'rb'))
        }

        kwargs["globalConfig"] = global_config
        self._validate({"compose_path": compose_path, "global_config": global_config}, "createAppByDockerCompose")

        return self._request.call("/app/group", params=kwargs, files=files, method="post")

    @staticmethod
    def __check_exist_file(file_path):
        if path.isfile(file_path):
            return

        raise InvalidDataException(message="file {} not exist".format(file_path), error_code=887)

    def get_group_with_name(self, group_name, **kwargs):
        """
        دریافت اطلاعات برنامه براساس نام گروه


        :param str group_name: نام گروه

        :return: dict
        """
        self._validate({"group_name": group_name}, "getGroupWithName")
        return self._request.call("/app/group/{}".format(group_name), params=kwargs)

    def create_pipeline(self, configs, **kwargs):
        """
        ایجاد برنامه با pipeline

        :param list configs: لیست تنظیمات

        :return: bool
        """

        self._validate({"configs": configs}, "createPipeline")
        self._request.call("/app/pipeline", params=kwargs, json=configs, method="post")
        return True

    def create_app_by_machine_mechanism(self, config, **kwargs):
        """
        ایجاد برنامه با مکانیزم ماشین حالت

        :param dict config: تنظیمات برنامه

        :return: bool
        """

        self._validate({"config": config}, "createAppByMachineMechanism")
        return self._request.call("/app/sm", json=config, params=kwargs, method="post")

    def get_user_apps_status_list(self, app_id=None, **kwargs):
        """
        دریافت وضعیت وضعیت برنامه ها

        :param int|None app_id: شناسه برنامه

        :return: list
        """
        if app_id is not None:
            kwargs["id"] = app_id

        data = kwargs.copy()
        self._validate(self.__delete_empty_item(data), "getUserAppsStatusList")
        return self._request.call("/app/status", params=kwargs)

    def stop_app_deploy_with_queue_id(self, deploy_queue_id, **kwargs):
        """
        توقف بارگزاری با استفاده از Queue Id

        :param str deploy_queue_id: UUID پردازش دیپلوی

        :return: str
        """
        self._validate({"deploy_queue_id": deploy_queue_id}, "stopAppDeployWithQueueId")
        return self._request.call("/app/stopDeploying?deployQueueId={}".format(deploy_queue_id), params=kwargs)

    @staticmethod
    def __delete_empty_item(config):
        return {key: value for key, value in config.items() if value is not None and value != "" and value != {}}
