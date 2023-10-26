from flask import Flask, render_template, flash, redirect, url_for
from app.config import MONGO_URI, SECRET_KEY
from app.model.user_model import mongo
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import datetime

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['MONGO_URI'] = MONGO_URI
app.config['JWT_SECRET_KEY'] = '38dd56f56d405e02ec0ba4be4607eaab'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
mongo.init_app(app)
jwt = JWTManager(app)
from app.routes.user_routes import user_bp
app.register_blueprint(user_bp)
if __name__ == "__main__":
    app.run(debug=True)