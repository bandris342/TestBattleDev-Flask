from flask import Flask
from app.models import db, User, Exercices, Startstop
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'super secret key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.username=='admin'
        else:
            return False

admin = Admin(app, name='Admin page', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(ModelView(Startstop, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Exercices, db.session))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

db.init_app(app)
db.create_all(app=app)

from app import views