
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig 

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

csrf = CSRFProtect()
migrate = Migrate()

def create_app(config_class=DevelopmentConfig): 
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
  
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    from app.admin import admin as admin_blueprint
    from app.pharmacist import pharmacist as pharmacist_blueprint
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(pharmacist_blueprint, url_prefix='/pharmacist')
    app.register_blueprint(main_blueprint)
    
    from app.chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)
    
    return app

from app import models