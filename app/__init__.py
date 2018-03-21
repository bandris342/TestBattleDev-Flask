from flask import Flask
from app.models import db, User, Exercices
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

admin = Admin(app, name='Admin page', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Exercices, db.session))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

db.init_app(app)
db.create_all(app=app)

from app import views