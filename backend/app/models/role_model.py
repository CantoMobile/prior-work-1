from flask import current_app


class Role:
    def __init__(self, name, description, permissions):
        self.name = name
        self.description = description
        self.permissions = permissions

    def __eq__(self, other):
            if isinstance(other, Role):
                return self.name == other.name
            return False
    