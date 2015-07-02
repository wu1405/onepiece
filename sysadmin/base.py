# coding=utf-8
import os
# 通常你不应该从django引入任何代码, 但ImproperlyConfigured是个例外
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)