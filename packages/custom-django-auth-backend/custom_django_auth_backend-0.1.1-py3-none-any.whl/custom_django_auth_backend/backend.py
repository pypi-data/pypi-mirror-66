from typing import Optional, Type

from django.forms import ValidationError

from .dto import UserDTO
from .exceptions import UnavailbleException, AuthException, WrongUserPasswordException, BlockedUserException
from .settings import DEFAULT_USERNAME_PREFIX
from .logging import logger


class BasicAuthBackend:
    # хранить ли пользовательские пароли в случае недоступности сервиса
    STORE_PASSWORDS = True
    USERNAME_PREFIX = DEFAULT_USERNAME_PREFIX

    def get_user_by_login(self, username: str, password: str) -> UserDTO:
        """Тут должна быть логика получения пользователя"""

        raise NotImplementedError

    def get_user_model(self) -> Type:
        try:
            from django.contrib.auth.models import User
            return User
        except Exception:
            logger.exception('Не удалось импортировать модель User')
            raise

    def get_user(self, user_id: int):
        return self.get_user_model().objects.filter(pk=user_id).first() or None

    def get_prefixed_username(self, username: str) -> str:
        return f'{self.USERNAME_PREFIX}{username}'

    def get_user_by_login_exists(self, username: str, password: str):
        if not self.STORE_PASSWORDS:
            return None
        user = self.get_user_model().objects.filter(username=self.get_prefixed_username(username)).first()
        if not user:
            return None
        if user.check_password(password):
            return user
        return None

    def get_and_update_user(self, username: str, password: str, user_dto: UserDTO):
        user, _ = self.get_user_model().objects.update_or_create(username=self.get_prefixed_username(username),
                                                                 defaults=user_dto.params)
        if not self.STORE_PASSWORDS:
            return user
        if not user.check_password(password):
            user.set_password(password)
            user.save()
        return user

    def delete_password_user_if_exists(self, username: str):
        self.get_user_model().objects.filter(
            username=self.get_prefixed_username(username)
        ).update(password='')

    def set_inactive_user_if_exists(self, username: str):
        self.get_user_model().objects.filter(
            username=self.get_prefixed_username(username)
        ).update(is_active=False)

    def authenticate(self, request, username: str, password: str) -> Optional['User']:
        if username is None or password is None:
            return None
        try:
            user_dto = self.get_user_by_login(username, password)
        except UnavailbleException:
            return self.get_user_by_login_exists(username, password)
        except WrongUserPasswordException as e:
            self.delete_password_user_if_exists(username)
            raise ValidationError(e.readable_error)
        except BlockedUserException as e:
            self.delete_password_user_if_exists(username)
            self.set_inactive_user_if_exists(username)
            raise ValidationError(e.readable_error)
        except AuthException:
            return None
        except Exception:
            logger.exception('Ошибка получения пользователя')
            return None
        return self.get_and_update_user(username, password, user_dto)
