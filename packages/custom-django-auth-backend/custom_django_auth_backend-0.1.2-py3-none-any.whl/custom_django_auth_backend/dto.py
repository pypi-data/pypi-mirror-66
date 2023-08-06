from typing import Optional


class UserDTO:
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: bool
    is_active: bool

    def __init__(self, first_name: str = None, last_name: str = None, is_admin: bool = None, is_active: bool = None):
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.is_active = is_active
        self.__post_init__()

    def __post_init__(self):
        if not isinstance(self.first_name, str):
            self.first_name = None
        if not isinstance(self.last_name, str):
            self.last_name = None
        if not isinstance(self.is_admin, bool):
            self.is_admin = False
        if not isinstance(self.is_active, bool):
            self.is_active = False

    @property
    def params(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_superuser': self.is_admin,
            'is_staff': self.is_admin,
            'is_active': self.is_active,
        }
