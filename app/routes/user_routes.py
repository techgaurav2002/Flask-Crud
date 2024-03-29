import hashlib
import json
import smtplib
import random
from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from app.controller.user_controller import UserController
from app.services.encoder import json_encoder_mongo
from app.services.send_email import send_otp_email,send_forgot_links

user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['GET'])
def get_users():
    controller = UserController()
    users = controller.get_users()
    data = list(users)
    return json.dumps(data, default=json_encoder_mongo)

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    controller = UserController()
    user_data = controller.get_user_by_id(ObjectId(user_id))
    # return render_template('user.html', user=user_data)
    # data = list(user_data)
    # return(data)
    # return("find one user")
    # return json.dumps(data, default=json_encoder_mongo)
    return json.dumps(user_data,default=json_encoder_mongo)



# def send_welcome_email(email):
#     # Replace these with your email server details
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     smtp_username = "hakergaurav.mkp2000@gmail.com"
#     smtp_password = "bpjyynjzwdvmekix"

#     from_email = "hakergaurav.mkp2000@gmail.com"
#     to_email = email

#     subject = "Welcome to Your App"
#     message = "Thank you for registering with our app. Your account has been created successfully."

#     try:
#         # Connect to the SMTP server
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(smtp_username, smtp_password)

#         # Send the email
#         server.sendmail(from_email, to_email, f"Subject: {subject}\n\n{message}")

#         # Close the connection
#         server.quit()
#         return True
#     except Exception as e:
#         print(f"Email sending error: {e}")
#         return False



@user_bp.route('/users', methods=['POST'])
def create_user():
    controller = UserController()
    user = request.json

    # Check if password and email are provided
    if not user.get("password"):
        return jsonify({'msg': 'Password is required'}), 409
    elif not user.get("email"):
        return jsonify({'msg': 'Email is required'}), 409

    # Validate email format
    import re
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_pattern, user["email"]):
        return jsonify({'msg': 'Invalid email format'}), 409

    # Validate password strength (e.g., minimum length)
    if len(user["password"]) < 8:
        return jsonify({'msg': 'Password must be at least 8 characters long'}), 409
    
    otp = str(random.randint(1000, 9999))

    if not send_otp_email(user["email"], otp):
        return jsonify({'msg': 'Error sending OTP email'}), 500
    # if not send_forgot_email(user["email"], otp):
    #     return jsonify({'msg': 'Error sending OTP email'}), 500


    # Hash the password
    user["password"] = hashlib.sha256(user["password"].encode("utf-8")).hexdigest()

    # Check if email already exists
    doc = controller.get_user_by_email(user.get("email"))
    
    if not doc:
        controller.create_user(user)
        # flash('User created successfully', 'success')
        # return redirect(url_for('user.get_users'))
        return jsonify({'msg': 'Registration Successfull'}), 202
    else:
        return jsonify({'msg': 'Email already exists'}), 409


@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    controller = UserController()
    # user_data = request.form.to_dict()
    # user_data = request.json
    controller.update_user(user_id, request.json)
    flash('User updated successfully', 'success')
    # return redirect(url_for('user.get_users'))
    return jsonify({"msg":"Update Sucessfull"})

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    controller = UserController()
    controller.delete_user(user_id)
    # flash('User deleted successfully', 'success')
    # return redirect(url_for('user.get_users'))
    return jsonify({"msg":"Delete Sucessfull"})

@user_bp.route('/login',methods=['POST'])
def login():
    controller = UserController()
    login_details = request.get_json()
    access_token = controller.loginAuthentication(login_details)
    if access_token:
        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'msg': 'Invalid email or password'}), 401

@user_bp.route('/forgot',methods=['POST'])
def forgot():
    controller = UserController()
    data = request.json
    link = controller.forgot_password(data.get("email"))
    if not send_forgot_links(data.get("email"), link):
        return jsonify({'msg': 'Error sending link on  email'}), 500
    return jsonify({'msg': 'Reset Link sent successfully'}), 401

@user_bp.route('/reset-password/<forgot_token>', methods=['POST'])
def reset_password(forgot_token):
    controller = UserController()
    data = request.json
    mesage =  controller.reset_password(forgot_token,data.get("newPassword"))
    return jsonify({'msg':mesage})
    
