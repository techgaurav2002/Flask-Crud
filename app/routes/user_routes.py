import json
from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for, flash,jsonify
from app.controller.user_controller import UserController
from app.services.encoder import json_encoder_mongo

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
    user_data = controller.get_user_by_id(user_id)
    # return render_template('user.html', user=user_data)
    data = list(user_data)
    return json.dumps(data,default=json_encoder_mongo)

@user_bp.route('/users', methods=['POST'])
def create_user():
    controller = UserController()
    # user_data = request.form.to_dict()
    # print(request.json)
    controller.create_user(request.json)
    flash('User created successfully', 'success')
    return redirect(url_for('user.get_users'))


@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    controller = UserController()
    # user_data = request.form.to_dict()
    # user_data = request.json
    controller.update_user(user_id, request.json)
    flash('User updated successfully', 'success')
    return redirect(url_for('user.get_users'))

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    controller = UserController()
    controller.delete_user(ObjectId(user_id))
    flash('User deleted successfully', 'success')
    return redirect(url_for('user.get_users'))