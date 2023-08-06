from .utils import get_from_settings_or_env as get


LOGGER_NAME = get('CUSTOM_AUTH_BACKEND_LOGGER_NAME', 'custom_django_auth_backend')
DEFAULT_USERNAME_PREFIX = get('CUSTOM_AUTH_BACKEND_DEFAULT_USERNAME_PREFIX', 'custom_')
