from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,RadioField,SelectField,TextAreaField
from wtforms.fields.html5 import EmailField, IntegerField,URLField,DateField
from wtforms.validators import DataRequired,Email,EqualTo, NumberRange,ValidationError,URL,Length
from app.models import User
from flask_login import current_user,login_user,logout_user,login_required

class LoginForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired(),Email()],render_kw={'class':'form-control form-group','placeholder':'email'})
    password=PasswordField('Password',validators=[DataRequired()],render_kw={'class':'form-control form-group','placeholder':'password'})
    remember_me=BooleanField('Keep Me Signed In')
    submit=SubmitField('Sign In',render_kw={'class':'btn btn-primary','style':'height : 50px;'})

class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()],render_kw={'class':'form-control form-group','placeholder':'Username'})
    email=EmailField('Email',validators=[DataRequired(),Email()],render_kw={'class':'form-control form-group','placeholder':'Email'})
    aadhar=StringField('Aadhar',validators=[DataRequired(),Length(min=12,max=12,message="Invalid Aadhar Number")],render_kw={'class':'form-control form-group','placeholder':'Aadhar'})
    mobile_number=StringField('Mobile Number',validators=[DataRequired(),Length(min=10,max=10,message="Invalid Phone Number")],render_kw={'class':'form-control form-group','placeholder':'Phone Number'})
    area_pincode=StringField('PINCODE',validators=[DataRequired(),Length(min=6,max=6,message="Invalid PIN Code")],render_kw={'class':'form-control form-group','placeholder':'PINCODE'})
    age=IntegerField('Age',validators=[DataRequired(),NumberRange(min=17)],render_kw={'class':'form-control form-group','placeholder':'Age'})
    gender=RadioField('Gender',choices=[('Male','Male'),('Female','Female'),('Others','Others')],validators=[DataRequired()],render_kw={'style':'list-style:none;'})
    password=PasswordField('Password',validators=[DataRequired()],render_kw={'class':'form-control form-group','placeholder':'Password'})
    conpassword=PasswordField('Re-Enter Password',validators=[DataRequired(),EqualTo('password')],render_kw={'class':'form-control form-group','placeholder':'Re-Enter Password'})#('values','label')
    submit=SubmitField('Sign In',render_kw={'class':'btn btn-primary','style':'height : 50px;'})
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please Use a Different Username.')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please Use A different Email Address')