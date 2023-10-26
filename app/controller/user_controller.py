import hashlib
import secrets
import time
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
    
    def forgot_password(self, email):
        user = self.model.get_user_by_email(email)
        if user:
            # Generate a unique reset token (can be a random string)
            reset_token = secrets.token_urlsafe(32)
            
            # Store the reset token and timestamp in the user's record in the database
            user['reset_token'] = reset_token
            user['reset_token_timestamp'] = time.time()  
            
            # Update the user's record in the database with the reset token
            self.model.update_user(ObjectId(user['_id']), user)

            # Send an email to the user with a link to reset their password
            reset_link = f"http://127.0.0.1:5000/reset-password/{reset_token}"
            return reset_link
        
    def reset_password(self, reset_token, new_password):
        RESET_TOKEN_EXPIRATION_TIME = 3600
        user = self.model.get_user_by_reset_token(reset_token)
        if user:
            # Check if the reset token is not expired (e.g., within a time limit)
            current_time = time.time()
            if 'reset_token_timestamp' in user and (current_time - user['reset_token_timestamp']) <= RESET_TOKEN_EXPIRATION_TIME:
                # Reset the password
                user['password'] = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
                
                # Remove the reset token and timestamp from the user's record
                del user['reset_token']
                del user['reset_token_timestamp']

                # Update the user's record in the database
                self.model.update_user(ObjectId(user['_id']), user)

                return 'Password reset successful'
            else:
                return 'Reset token has expired'
        else:
            return 'Invalid reset token'