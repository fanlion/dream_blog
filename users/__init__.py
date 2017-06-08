from django.apps import AppConfig
from os import path

"""
修改应用名称，以中文显示在后台
"""

VERBOSE_APP_NAME = '用户管理'


def get_current_app_name(_file):
    return path.split(path.dirname(_file))[-1]


class AppVerboseNameConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = VERBOSE_APP_NAME


default_app_config = get_current_app_name(__file__) + '.__init__.AppVerboseNameConfig'
