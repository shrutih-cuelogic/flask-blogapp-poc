from flask_wtf import FlaskForm
from wtforms import (
StringField, 
TextAreaField, 
PasswordField, 
IntegerField, 
RadioField, 
SelectField,
SubmitField,
BooleanField,
validators
) 

GENDER =[('Male','M'),('Female','F')]

# Register Form Class
class RegisterForm(FlaskForm):
    """ Registerform for registering users """
    name = StringField('*Name', [validators.Length(min=1, max=50)])
    username = StringField('*Username', [validators.Length(min=4, max=25)])
    email = StringField('*Email', [validators.Length(min=6, max=50)])
    password = PasswordField('*Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('*Confirm Password',[validators.DataRequired()])
    address = TextAreaField('Address', [validators.optional(), validators.length(max=200)])
    submit= SubmitField("Register")

# Login Form Class
class LoginForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=1, max=64)])
    password = PasswordField('Password',[validators.DataRequired()])
    remember_me = BooleanField('Remember me',default=False)
    submit= SubmitField("Log In")

# Profile Edit Form Class
class ProfileEditForm(FlaskForm):
    """ PrfoileEditform for editing users profile """
    username = StringField("Username",[validators.DataRequired()])
    email = StringField("Email",[validators.DataRequired(), validators.Length(1,64),validators.Email()])
    contact = IntegerField("Contact",[validators.optional()])
    address = TextAreaField("Address")
    gender = SelectField("Gender",choices=GENDER)
    submit= SubmitField("Save Profile")
