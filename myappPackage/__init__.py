from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key='Secret Key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

bcrypt = Bcrypt(app)
login_manger = LoginManager(app)
migrate = Migrate(app,db)

from myappPackage import routes