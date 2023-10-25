from bson import ObjectId
from app.model.user_model import User

class UserController:
    def __init__(self):
        self.model = User()

    def create_user(self, user_data):
        return self.model.create_user(user_data)

    def get_users(self):
        return self.model.get_users()

    def get_user_by_id(self, user_id):
        return self.model.get_user_by_id(user_id)

    def update_user(self, user_id, user_data):
        return self.model.update_user(ObjectId(user_id), user_data)

    def delete_user(self, user_id:ObjectId):
        return self.model.delete_user(ObjectId(user_id))