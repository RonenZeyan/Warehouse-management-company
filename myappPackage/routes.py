import secrets
from myappPackage.models import Product,User,Post,Comment
from flask import render_template,request,redirect,url_for,flash,abort,jsonify
from myappPackage.forms import RegisterationForm,LoginForm,UpdateProfileForm,NewProductForm,NewPostForm,UpdatePostForm,SearchUsersForm,RequestPasswordResetForm,PasswordResetForm,NewCommentForm
from myappPackage import app,bcrypt,db
from flask_login import login_user,current_user,logout_user,login_required
import os
from flask_mail import Mail
from sqlalchemy import desc


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
        products = Product.query.filter_by(ownerID=current_user.id).all()
        return render_template('test.html',products=products)
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
    new_product_form = NewProductForm()
    if new_product_form.validate_on_submit():
        productname = new_product_form.productName.data
        product = Product(productName=productname,price=new_product_form.price.data,count=new_product_form.count.data,ownerID=current_user.id)
        db.session.add(product)
        db.session.commit()
        flash('your product added successfully')
        return redirect(url_for("index"))
        
    return render_template('insertProd.html',form=new_product_form)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    page = request.args.get("page", 1, type=int)
    # posts = Post.query.paginate(page=page,per_page=7)
    posts = Post.query.order_by(desc(Post.id)).paginate(page=page,per_page=7)
    users = User.query.all()
    return render_template('posts.html',posts=posts,users=users)

@app.route('/SearchUsers',methods=['GET','POST'])
def search_users():
    page = request.args.get("page", 1, type=int)
    users = User.query.paginate(page=page,per_page=5)
    search_user_form = SearchUsersForm()
    if search_user_form.validate_on_submit():
        search_username = search_user_form.insertedUser.data
        # users = User.query.filter_by(username=search_username).paginate(page=page,per_page=5)
        users_query = User.query.filter(User.username.ilike(f"%{search_username}%"))
        users = users_query.paginate(page=page, per_page=5)
    return render_template('SearchUser.html',users=users,form=search_user_form)

@app.route('/posts/<id>', methods=['GET','POST'])
def displayPost(id):
    mydata = Post.query.get_or_404(id)
    user= User.query.filter_by(id=mydata.ownerID).first()
    page = request.args.get("page", 1, type=int)
    comment = Comment.query.filter_by(postID=id).paginate(page=page,per_page=5)
    users = User.query.all()
    form = NewCommentForm()
    if form.validate_on_submit():
        commenting=Comment(content=form.content.data,ownerID=current_user.id,postID=id) 
        db.session.add(commenting)
        db.session.commit()
        return redirect(url_for('displayPost',id=id))
    return render_template('postView.html',mydata=mydata,user=user,form=form,comments=comment,users=users,id=id)

@app.route('/posts/create_post', methods=['GET','POST'])
@login_required
def create_post():
    new_post_form = NewPostForm()
    if new_post_form.validate_on_submit():
        postTitle = new_post_form.title.data
        post = Post(title=postTitle,content=new_post_form.content.data,ownerID=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('your Post added successfully')
        return redirect(url_for("posts"))

    return render_template('create_post.html',form=new_post_form)


@app.route('/posts/user_posts',methods=['GET','POST'])
def user_posts():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.filter_by(ownerID=current_user.id).paginate(page=page,per_page=5)
    return render_template('userPosts.html',posts=posts)

# /<title>
@app.route('/posts/user_posts/<title>/update',methods=['GET','POST'])
def update_post(title):
    get_post = Post.query.filter_by(title=title).first()
    post_id = get_post.id if get_post else None
    post = Post.query.get_or_404(post_id)
    if post.ownerID !=current_user.id:
        abort(403) #in case another user trying to access another user post
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('update done successfully!!')
        return redirect(url_for('user_posts'))
    elif request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('updatePost.html',form=form)

@app.route('/posts/user_posts/<title>/accept_delete',methods=['GET','POST'])
def delete_post(title):
    get_post = Post.query.filter_by(title=title).first()
    post_id = get_post.id if get_post else None
    post = Post.query.get_or_404(post_id)
    if post.ownerID !=current_user.id:
        abort(403) #in case another user trying to access another user post
    db.session.delete(post)
    db.session.commit()
    flash('delete done successfully')
    return redirect(url_for('user_posts'))


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
        if(current_user.profileIMG=='defaultUserPhoto.png'):
            image_file=None
    return render_template('updateProfile.html',profile_form=profile_form,image_file=image_file)

@app.route('/user/<username>',methods=['GET'])
def displayuser(username):
    myuser = User.query.filter_by(username=username).first()
    mydata_id = myuser.id if myuser else None
    mydata = User.query.get_or_404(mydata_id)
    return render_template('profileView.html',mydata=mydata)

@app.route('/reset_password',methods=['GET','POST'])
def resetPassword():
    #check that user not login 
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            #send_change_password(user)
            flash('you will recive an email for change password,in case this account is exist!!')
            return redirect(url_for('login'))
    return render_template('requestResetPassword.html',form=form)

@app.route('/reset_password/<token>',methods=['POST'])
def ChangePassword(token):
    #check that user not login 
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if not user:
        flash('the token is expired')
        return redirect(url_for('resetPassword'))
    form = PasswordResetForm()
    return render_template('changeForgottenPassword.html',form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/rent')
def rent():
    return render_template('rent.html')

@app.route('/rent/rentNow/<StorageType>')
def rentNow(StorageType):
    pass
    # mydata = Post.query.get_or_404(id)
    # user= User.query.filter_by(id=mydata.ownerID).first()
    # page = request.args.get("page", 1, type=int)
    # comment = Comment.query.filter_by(postID=id).paginate(page=page,per_page=5)
    # form = NewCommentForm()
    # if form.validate_on_submit():
    #     pass
    # return render_template('postView.html',mydata=mydata,user=user,form=form,comments=comment)


@app.route('/get_data/<username>', methods=['GET','POST'])
def get_data(username):
    x = User.query.filter_by(username=username).first()
    if x:
        data = {"DONT":"yesUser"}
    else:
        data = {"DONT":"noUser"}
    return jsonify(data)



@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'),403
@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'),404
@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'),500