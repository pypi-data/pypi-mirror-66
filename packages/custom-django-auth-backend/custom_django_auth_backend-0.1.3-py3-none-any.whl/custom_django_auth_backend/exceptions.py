class AuthException(Exception):
    base_name = 'Ошибка подключения'

    def __init__(self, *args, **kwargs):
        if not args:
            args = (self.base_name, )
        else:
            self.base_name = str(args[0])
        super().__init__(*args, **kwargs)

    @property
    def readable_error(self):
        return self.base_name


class WrongUserPasswordException(AuthException):
    base_name = 'Неверный логин или пароль'


class BlockedUserException(AuthException):
    base_name = 'Пользователь заблокирован'


class UnavailbleException(AuthException):
    base_name = 'Не удалось подключиться, сервис недоступен или имеет неккоректный ответ'
