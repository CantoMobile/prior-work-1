
class Permissions:
    def __init__(self, resource, actions, _id= None):
        self.resource = resource
        self.actions = actions
        if _id is not None:
            if isinstance(_id, str):
                self._id = _id
            else:
                self._id = _id 
        