from flask_pymongo import PyMongo

mongo = PyMongo()

class User:
    def create_user(self, user_data):
        users = mongo.db.user
        user_id = users.insert_one(user_data)
        return user_id

    def get_users(self):
        users = mongo.db.user
        return users.find()

    def get_user_by_id(self, user_id):
        users = mongo.db.user
        return users.find_one({'_id': user_id})

    def update_user(self, user_id, user_data):
        users = mongo.db.user
        return users.update_one({'_id': user_id}, {'$set': user_data})

    def delete_user(self, user_id):
        users = mongo.db.user
        delte = users.delete_one({'_id': user_id})
        return users.delete_one({'_id': user_id})
    def get_user_by_email(self,email):
        users = mongo.db.user
        return users.find_one({'email':email})
    def get_user_by_reset_token(self,token):
        users = mongo.db.user
        return users.find_one({'reset_token':token})