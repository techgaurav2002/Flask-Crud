import hashlib
from bson import ObjectId
from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
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
    def get_user_by_email(self,email):
        return self.model.get_user_by_email(email)
    
    def loginAuthentication(self,login_detail):
        # print("***********loginDetail",login_detail.get("email"))
        user_from_db = self.model.get_user_by_email(login_detail.get("email"))
        if user_from_db:
            # checking password
            encrpted_password = hashlib.sha256(login_detail.get("password").encode("utf-8")).hexdigest()
            print("user enter",encrpted_password)
            print("inside database",user_from_db['password'])
            if encrpted_password == user_from_db['password']:
                print("gaurav")
                # Create JWT Access Token
                access_token = create_access_token(identity=user_from_db['email'])
                return access_token
        
        return None