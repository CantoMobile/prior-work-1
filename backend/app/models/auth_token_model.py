import datetime


class AuthToken:
    def __init__(self, user, token):
        self.user = user
        self.token = token
        self.created_at = datetime.datetime.now()

    def validate(self):
        required_fields = ['user', 'token']
        for field in required_fields:
            if field not in self:
                raise ValueError(f"Missing required field: {field}")
