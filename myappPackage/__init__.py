from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor


app = Flask(__name__)
app.secret_key='Secret Key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/warehousedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
db = SQLAlchemy(app)
app.app_context().push()
app.config['MAIL_SERVER']= 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
bcrypt = Bcrypt(app)
login_manger = LoginManager(app)
ckeditor = CKEditor(app)
migrate = Migrate(app,db)

from myappPackage import routes