import os
import wrapt

from .logging import logger


DEFAULT_BACKEND = 'django.contrib.auth.backends.ModelBackend'


def check_is_autowrapt(name: str) -> bool:
    return name in os.getenv('AUTOWRAPT_BOOTSTRAP', '').split(',') or True


def add_backend_if_not_exists(backend_path: str):
    from django.conf import settings
    if backend_path not in settings.AUTHENTICATION_BACKENDS:
        if type(settings.AUTHENTICATION_BACKENDS) is tuple:
            settings.AUTHENTICATION_BACKENDS = (backend_path, ) + settings.AUTHENTICATION_BACKENDS
        elif type(settings.AUTHENTICATION_BACKENDS) is list:
            settings.AUTHENTICATION_BACKENDS = [backend_path, ] + settings.AUTHENTICATION_BACKENDS
        else:
            logger.error('Could not import %s to django', backend_path)


def wrapt_authentication_backend(backend_class):
    module_name = backend_class.__module__
    class_name = backend_class.__name__
    backend_path = f'{module_name}.{class_name}'

    if not check_is_autowrapt(module_name):
        return

    def load_backends_wrapper(wrapped, instance, args, kwargs):
        add_backend_if_not_exists(DEFAULT_BACKEND)
        add_backend_if_not_exists(backend_path)
        return wrapped(*args, **kwargs)

    wrapt.wrap_function_wrapper('django.contrib.auth', '_get_backends', load_backends_wrapper)
