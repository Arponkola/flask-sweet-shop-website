import flask
from flask import request, render_template, Blueprint, redirect, url_for, session
from app.extension import bcrypt
from app.model.user import search_from_login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

login_bp = Blueprint(
        "login_route",
        __name__,
        static_folder='static',
        template_folder='templates'
    )

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw = {"class" : "form-control", "placeholder" : "Email Address"}
    )
    
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"class" : "form-control", "placeholder": "Password"}
    )
    
    submit = SubmitField(
        "Login",
        render_kw={"class":"btn btn-primary"}
    )


@login_bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        useremail = form.email.data
        password = form.password.data
        
        if useremail:
            user = search_from_login_user(useremail)
            
            if not user:
                return redirect(url_for('login_route.login'))
            
            if bcrypt.check_password_hash(user.password, password) and useremail==user.email:
                session["user"] = useremail
                session["is_admin"] = user.is_admin
                    
                return redirect(url_for('home_route.home'))
            
    return render_template("login.html", form=form) #render html content of login page

@login_bp.route('/logout/')
def logout():
    if'user' in session:
        session.clear()
    return redirect(url_for('home_route.home'))