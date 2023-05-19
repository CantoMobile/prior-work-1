import datetime
from models.authentication_model import Authentication


class User:
    def __init__(self, name, email, password, auth_id=None, auth_provider=None, sites=None, roles=None, created_at=None):
        self.name = name
        self.email = email
        self.password = password
        self.auth_id = auth_id
        self.auth_provider = auth_provider
        self.sites = sites or []
        self.roles = roles or []
        if created_at is None:
            self.created_at = datetime.datetime.now()
        else:
            self.created_at = created_at

    def verify_password(self, password):
        return self.password == password

    def set_password(self, password):
        if self.password == password:
            return None
        elif len(password) > 8:
            self.password = password
            return True
        else:
            return False

    def add_role(self, role):
        print(len(self.roles))
        if any(existing_role.name == role.name for existing_role in self.roles):
            return False
        else:
            self.roles.append(role)
            return True

    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role._to__dict__)

    def has_permission(self, permission):
        for role in self.roles:
            if permission in role.permissions:
                return True
        return False
