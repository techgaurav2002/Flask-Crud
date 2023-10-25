from flask import Flask, render_template, flash, redirect, url_for
from app.config import MONGO_URI, SECRET_KEY
from app.model.user_model import mongo

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['MONGO_URI'] = MONGO_URI
mongo.init_app(app)

from app.routes.user_routes import user_bp
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)