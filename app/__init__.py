import click

from flask import Flask
from flask.cli import AppGroup
from config import Config
from app.extensions import db, Migrate, LoginManager

import flask_login
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class ModelView(ModelView):
    def is_accessible(self):
        is_admin = False
        try:
            is_admin = flask_login.current_user.admin
        except AttributeError:
            is_admin = False
        return is_admin

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Flask Extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "You need to be logged in to view the page..."
    login_manager.init_app(app)

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    admin = Admin(app, name="Flask-App", template_mode="bootstrap4")
    admin.add_view(ModelView(User, db.session))

    # CLI Commands
    database_cli = AppGroup('database')

    @database_cli.command('create')
    def create_database():
        db.create_all()

    @database_cli.command('delete')
    def delete_database():
        db.drop_all()

    @database_cli.command('superuser')
    @click.argument('user_email')
    def make_superuser(user_email):
        user = User.query.filter_by(email=user_email).first()
        if user:
            print(f"Making {user.name} into admin")
            user.admin = True
            db.session.commit()
        else:
            print("User not found with email f{user_email}")

    app.cli.add_command(database_cli)
    # Blueprints

    from app.auth import bp as auth_routes_bp
    app.register_blueprint(auth_routes_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
