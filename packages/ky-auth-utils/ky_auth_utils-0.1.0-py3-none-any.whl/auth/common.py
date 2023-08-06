import json


class Auth:

    USER_ID_KEY = 'USER-ID'
    USERNAME_KEY = 'USERNAME'
    USER_OBJ_KEY = 'USER-OBJ'
    ROLES_KEY = 'ROLES'

    def __init__(self, user_id: str, username: str, user_obj: dict, roles):
        self._user_id = user_id
        self._username = username
        self._user_obj = user_obj
        self._roles = self.format_roles(roles)

    @staticmethod
    def format_roles(roles):
        if isinstance(roles, str):
            return roles.split(',')
        elif isinstance(roles, list):
            return roles
        return []

    @classmethod
    def from_dict(cls, data, prefix='X-AUTH-'):
        key = prefix + cls.USER_ID_KEY
        user_id = data[key] if key in data and data[key] else None
        key = prefix + cls.USERNAME_KEY
        username = data[key] if key in data and data[key] else None
        key = prefix + cls.USER_OBJ_KEY
        user_obj = data[key] if key in data and data[key] else None
        if user_obj:
            try:
                user_obj = json.loads(user_obj)
            except json.JSONDecodeError:
                user_obj = None
        key = prefix + cls.ROLES_KEY
        roles = data[key] if key in data and data[key] else None
        return cls(user_id=user_id, username=username, user_obj=user_obj, roles=roles)

    def to_dict(self, prefix='X-AUTH-'):
        data = dict()
        key = prefix + self.USER_ID_KEY
        if self.user_id:
            data[key] = self.user_id
        key = prefix + self.USERNAME_KEY
        if self.username:
            data[key] = self.username
        key = prefix + self.USER_OBJ_KEY
        if self.user:
            data[key] = json.dumps(self.user, ensure_ascii=False)
        key = prefix + self.ROLES_KEY
        if self.roles:
            data[key] = ','.join(self.roles)
        return data

    def has_role(self, role):
        return role in self._roles

    def is_login(self):
        return self.user_id is not None and len(self.user_id) > 0

    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self):
        return self._username

    @property
    def user(self):
        return self._user_obj

    @property
    def roles(self):
        return self._roles

    def __str__(self):
        return self.to_dict()
