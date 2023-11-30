
from myappPackage.models import Product,User
from flask import render_template,request,redirect,url_for,flash
from myappPackage.forms import RegisterationForm,LoginForm
from myappPackage import app,bcrypt,db

@app.route('/')
def index():
    # mydata = Data.query.all()
    return render_template('test.html')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #make the password hashed
        user = User(username=form.Username.data,firstName=form.firstname.data,lastName=form.lastname.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
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