from flask import current_app


class Authentication:

    def __init__(self, email, password_hash):

        self.email = email
        self.password_hash = password_hash

    def save(self):
        with current_app.app_context():
            collection = current_app.mongo.authentications
        result = collection.insert_one({
            'email': self.email,
            'password_hash': self.password_hash
        })
        return result.inserted_id

    @staticmethod
    def find_by_email(email):
        with current_app.app_context():
            collection = current_app.mongo.authentications
        authentication = collection.find_one(
            {'email': email})
        if authentication:
            return Authentication(authentication['email'], authentication['password_hash'])
        return None
