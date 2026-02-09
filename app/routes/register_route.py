import flask
from flask import request, flash, render_template, Blueprint, redirect, url_for
from app.extension import bcrypt
from app.model.user import add_login_details
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

register_bp = Blueprint(
        "register_route",
        __name__,
        static_folder='static',
        template_folder='templates'
    )

#registration form class

class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=20)],
        render_kw={"class" : "form-control", "placeholder" : "Username"}
    )
    
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control", "placeholder" : "Email address"}
    )
    
    mobile = StringField(
        "Mobile Number",
        validators=[
            DataRequired(),
            Regexp(r'^[6-9]\d{9}$', message="Enter valid 10-digit mobile number")
        ],
        render_kw={"class":"form-control", "placeholder":"Mobile Number"}
    )
        
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"class" : "form-control", "placeholder": "Password"}
    )
    
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class":"form-control", "placeholder":"Confirm password"}
    )
    
    submit = SubmitField(
        "Register",
        render_kw={"class":"btn btn-primary"}
    )
    


@register_bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        usergmail = form.email.data
        usermobile = form.mobile.data
        password = form.password.data
        
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        if username and usergmail and usermobile:
            add_login_details(username, usergmail, password, usermobile)
            return redirect(url_for('login_route.login'))
    
    return render_template("register.html", form=form) #render html content of registation page