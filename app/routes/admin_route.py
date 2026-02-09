from flask import Blueprint, render_template, session, redirect, url_for, request
from functools import wraps
from app.model.user import LoginUsers
from app.model.fav import Favourite
from app.model.products import Product
from app.model.order import Orders
from app.extension import db, bcrypt
import re

admin_bp = Blueprint(
    "admin_route", __name__,
    template_folder='templates',
    static_folder='static'
)
    

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session or not session.get('is_admin'):
            return '''  <center>
                            <h1 style="color:red;">
                                Access Denied — Admin Only
                            </h1>
                        </center>''', 403
        return f(*args, **kwargs)
    return wrapper

@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    tusers = LoginUsers.query.all()
    products = Product.query.all()
    orders = Orders.query.filter_by(status="pending").all()
    return render_template('adminpanel.html', users=tusers, sweets=products, orders=orders)


#users
@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def users():
    tusers = LoginUsers.query.all()
    return render_template("admin_users.html", users=tusers)

@admin_bp.route('/admin/users/update', methods=['GET', 'POST'])
@admin_required
def users_update():
    user_id = request.args.get('user_id')
    
    if not is_valid_user_id(user_id):
        return "Invalid User Id"
    
    user_id = int(user_id)
    
    user_details = LoginUsers.query.get(user_id)
    if user_details.is_admin:
        admin = "yes"
    else:
        admin="no"
    
    if request.method=="POST":
        user_id = request.args.get('user_id')
        
        if not is_valid_user_id(user_id):
            return "Invalid User Id"
        
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin')
        
        valid, msg = validate_name(name)
        if not valid:
            return render_template('update_form.html', user_details=user_details, admin=admin, error=msg)
        
        valid, msg = validate_email(email)
        if not valid:
            return render_template('update_form.html', user_details=user_details, admin=admin, error=msg)
        
        valid, msg = validate_phone(mobile)
        if not valid:
            return render_template('update_form.html', user_details=user_details, admin=admin, error=msg)
        
        user = LoginUsers.query.get(int(user_id))
        user.name = name
        user.email = email
        user.mobile_number = mobile
        if not password:
            password = user.password
            user.password = password
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.is_admin =  1 if str(is_admin).lower() in ["yes", "true", "1", "on"] else 0
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return redirect(url_for('admin_route.users'))
    
    return render_template('update_form.html', user_details=user_details, admin=admin)
        

@admin_bp.route('/admin/users/delete', methods=['POST'])
@admin_required
def users_delete():
    uid = request.args.get('user_id').strip()
    if uid:
        uid = int(uid)
        all_users = LoginUsers.query.all()
        all_ids = []
        for uobj in all_users:
            all_ids.append(uobj.userId)
        
        if uid in all_ids:
            u = LoginUsers.query.filter(LoginUsers.userId==uid).first()
            db.session.delete(u)
            db.session.commit()
            if session["user"] == u.email:
                return redirect(url_for("login_route.logout"))
    
    return redirect(url_for("admin_route.users"))

@admin_bp.context_processor
def inject_fav_count():
    if 'user' in session:
        email = session.get('user')
        fav_count = Favourite.query\
            .filter_by(user_email=email)\
                .count()
        return dict(fav_count=fav_count)
    return dict(fav_count=0)

def is_valid_user_id(user_id:str):
    if not user_id:
        return False
    user_id = user_id.strip(' ')
    try:
        user_id = int(user_id)
    except Exception as e:
        return False
    return True

def validate_name(name:str):
    if not name:
        return False, "Name is required"
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"
    
    if not re.match(r"^[A-Za-z ]+$", name):
        return False, "Name can contain only letters and spaces"
    
    return True, ""

def validate_email(email:str):
    if not email:
        return False, "Email is required"
    
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, ""

def validate_phone(phone:str):
    if not phone:
        return False, "Phone number is required"
    
    if not re.match(r"^[6-9]\d{9}$", phone):
        return False, "Invalid phone number"
    
    return True, ""