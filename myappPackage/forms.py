from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo,ValidationError

from myappPackage.models import User

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
