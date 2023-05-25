from bson import ObjectId


class Role:
    def __init__(self, name, description, permissions, _id=None):
        self.name = name
        self.description = description
        self.permissions = permissions or []
        if _id is not None:
            if isinstance(_id, str):
                # self._id = ObjectId(_id)
                self._id = _id
            else:
                self._id = _id

    def __eq__(self, other):
        if isinstance(other, Role):
            return self.name == other.name
        return False
