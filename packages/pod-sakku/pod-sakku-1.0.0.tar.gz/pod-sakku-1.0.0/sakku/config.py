# coding=utf-8
import configparser


class Config:
    __config = None

    def __init__(self, config_path):
        self._config_path = config_path
        self.__read_config()

    def __read_config(self):
        """
        خواند تنظیمات از فایل کانفیگ
        """
        if Config.__config is not None:
            return

        Config.__config = configparser.ConfigParser()
        Config.__config.read(self._config_path)

    @staticmethod
    def get(key, default=""):
        """
        دریافت تنظیمات از فایل کانفیگ

        :param str|unicode key:
        :param str|unicode default:
        :return:
        """

        if key in Config.__config:
            return Config.__config[key]

        return default
