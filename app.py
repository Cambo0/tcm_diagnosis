from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, User
from auth import auth as auth_blueprint
from admin import admin as admin_blueprint
from main import main as main_blueprint
from diagnosis import diagnosis as diagnosis_blueprint
import logging

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(diagnosis_blueprint)
app.register_blueprint(main_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    logging.basicConfig(filename='tcm_diagnosis.log', level=logging.INFO)
    app.run(debug=True)