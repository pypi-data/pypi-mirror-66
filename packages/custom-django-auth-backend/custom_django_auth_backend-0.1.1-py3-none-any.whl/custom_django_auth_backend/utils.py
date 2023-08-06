import os
import logging
from lazy_object_proxy import Proxy

from django.core.exceptions import ImproperlyConfigured


def get_from_settings_or_env(name: str, default=None, cast=None):
    def get_value():
        try:
            from django.conf import settings
            getattr(settings, 'SOMEVALUE', None)
        except ImproperlyConfigured:
            # Где использовался не ленивый объект и значение пытается получиться до того,
            # как сконфигурировалась джанга
            settings = None
        value = getattr(settings, name, os.getenv(name, default))
        return cast(value) if cast and value is not None else value
    return Proxy(get_value)


def get_lazy_object(func, *args, **kwargs):
    return Proxy(lambda: func(*args, **kwargs))


def get_logger(name: str):
    return Proxy(lambda: logging.getLogger(__name__))
