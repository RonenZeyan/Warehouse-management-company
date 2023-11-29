from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterationForm,LoginForm

app = Flask(__name__)
app.secret_key='Secret Key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    productName = db.Column(db.String(100))
    price = db.Column(db.Double)
    count = db.Column(db.Integer)
    ownerID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    def __init__(self,productName,price,count):
        self.productName=productName
        self.price=price
        self.count=count

class User(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    firstName = db.Column(db.String(100),nullable=False)
    lastName = db.Column(db.String(100),nullable=False)
    profileIMG = db.Column(db.String(20),nullable=False,default="static/images/defaultUserPhoto.png")
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    products = db.relationship('Product',backref='owner',lazy=True) #user have one to many relationship

    def __init__(self,username,email):
        self.username=username
        self.email=email




@app.route('/')
def index():
    # mydata = Data.query.all()
    return render_template('test.html')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        flash(f"account created successfully for {form.Username.data}")
        return redirect(url_for('index'))
    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if(form.email.data =='ronen@gmail.com'
        and form.password.data == '123456'):
            flash('you have been logged in successfully!') 
            return redirect(url_for('index'))
        else:
            flash('one or more fields is not correct')
    return render_template('login.html',form=form)


@app.route('/products',methods=['GET','POST'])
def InsertProducts():
    if request.method == 'POST':
        name = request.form['productName']
        price = request.form['productPrice']
        count = request.form['productCount']
        mydata = Product(name,price,count)
        db.session.add(mydata)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('insertProd.html')


# @app.route('/insert',methods=['GET','POST'])
# def insert():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         mydata = Data(name,email,phone)
#         db.session.add(mydata)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('insert.html')

# @app.route('/testing/<id>')
# def displayuser(id):
#     mydata = Data.query.get(id)
#     return render_template('display.html',mydata=mydata)
    


if __name__ == "__main__":
    app.run(debug=True)