from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,FloatField,IntegerField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo,ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user
from myappPackage.models import User
from flask_wtf.file import FileField,FileAllowed
from flask_ckeditor import CKEditorField

class RegisterationForm(FlaskForm):
    firstname=StringField('First Name: ',validators=[DataRequired(),Length(min=2,max=25)])
    lastname=StringField('Last Name: ',validators=[DataRequired(),Length(min=2,max=25)])
    Username=StringField('Username: ',validators=[DataRequired(),Length(min=2,max=25)])
    email = StringField('Email: ',validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_Username(self,Username):
        user = User.query.filter_by(username=Username.data).first()
        if user:
            raise ValidationError("Username is already exists,Please choose another name!!!")
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("email is already exists,Please choose another email!!!")

class LoginForm(FlaskForm):
    email = StringField('Email:',validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired()])
    remember = BooleanField('Remember Me!!')
    submit = SubmitField('Login')



class UpdateProfileForm(FlaskForm):
    Username=StringField('Username: ',validators=[DataRequired(),Length(min=2,max=25)])
    email = StringField('Email: ',validators=[DataRequired(),Email()])
    bio = TextAreaField('Biography')
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField('Update')

    def validate_Username(self,Username):
        if Username.data != current_user.username:
            user = User.query.filter_by(username=Username.data).first()
            if user:
                raise ValidationError("Username is already exists,Please choose another name!!!")
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("email is already exists,Please choose another email!!!")



class NewProductForm(FlaskForm):
    productName = StringField('ProductName:',validators=[DataRequired(),Length(max=100)])
    price = FloatField('ProductPrice',validators=[DataRequired()])
    count = IntegerField('Count',validators=[DataRequired()])
    submit = SubmitField('Add')


class NewPostForm(FlaskForm):
    title = StringField('Post Title:',validators=[DataRequired(),Length(max=100)])
    content = CKEditorField('Content Title:',validators=[DataRequired()],render_kw={'rows': '30'})
    
    submit = SubmitField('Post')