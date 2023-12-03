import secrets
from myappPackage.models import Product,User
from flask import render_template,request,redirect,url_for,flash
from myappPackage.forms import RegisterationForm,LoginForm,UpdateProfileForm
from myappPackage import app,bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
import os

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/images',picture_name)
    form_picture.save(picture_path)
    return picture_name

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('test.html')
    else:
        return render_template('home.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data): #check if user exist in db and check if the password is correct
            login_user(user,remember=form.remember.data)
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


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/updateProfile',methods=['GET','POST'])
@login_required
def updateProfile():
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data)
            current_user.profileIMG = picture_file
        current_user.username = profile_form.Username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == "GET":
        profile_form.Username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.bio.data = current_user.bio
        image_file = url_for('static',filename=f'images/{current_user.profileIMG}')
        if(current_user.profileIMG=='static/images/defaul'):
            image_file=None
    return render_template('updateProfile.html',profile_form=profile_form,image_file=image_file)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


