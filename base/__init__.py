import os
from flask import Flask
from base.database.db import initialize_db
from dotenv import load_dotenv

from flask_login import LoginManager


load_dotenv()


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['UPLOAD_FOLDER']="base/static/profile_pic/"
    
    initialize_db(app)
    login_manager.init_app(app)

    from base.api.user.auth import user_auth
    from base.admin.auth import admin_auth
    from base.admin.view import admin_view
    from base.admin.create import admin_create
    from base.api.user.create import user_create  
    from base.api.user.view import user_view


    app.register_blueprint(user_auth)
    app.register_blueprint(admin_auth)
    app.register_blueprint(admin_view)
    app.register_blueprint(admin_create)
    app.register_blueprint(user_create)
    app.register_blueprint(user_view)


    return app