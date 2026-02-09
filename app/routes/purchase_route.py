from flask import Blueprint, request, render_template, session, redirect, url_for
from app.model.products import Product
from app.model.user import LoginUsers
from app.model.order import Orders
from app.model.products import Product
from app.model.fav import Favourite
from app.extension import db
import re

purchase_bp = Blueprint('purchase_route', __name__,
    template_folder='templates',
    static_folder='static')

@purchase_bp.route('/purchase/', methods=['GET', 'POST'])
def purchase():
    product_id = request.args.get('product_id')
    selected_product = Product.query.filter(Product.id == product_id).first()
    all_products = Product.query.all()

    products_data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        }
        for p in all_products
    ]
    
    return render_template(
        "purchase.html",
        selected = selected_product,
        products = products_data,
        session = session,
    )
    

@purchase_bp.route('/confirm-order', methods=['POST'])
def confirm_order():
    if 'user' not in session:
        name = request.form.get('name')
        uemail = request.form.get('email')
        phone = request.form.get('phone')
    else:
        uemail = session.get('user')
        user = LoginUsers.query.filter_by(email=uemail).all()
        phone = user[0].mobile_number
        name = user[0].name
    
    valid, msg = validate_name(name=name)
    
    if not valid:
        return msg, 404
    
    valid, msg = validate_email(email=uemail)
    
    if not valid:
        return msg, 404
    
    valid, msg = validate_phone(phone=phone)
    
    if not valid:
        return msg, 404
    
    sweet_ids = list(map(int, request.form.getlist('product_id[]')))
    sweet_qtys = list(map(int, request.form.getlist('qty[]')))
    
    products = Product.query.filter(Product.id.in_(sweet_ids)).all()
    product_map = {p.id: p for p in products}
    
    total = 0
    
    for pid, qty in zip(sweet_ids, sweet_qtys):
        product = product_map.get(pid)

        if product.stock < qty:
            return "Out Of Stocks"
        
        uorder = Orders(
            product_id=pid,
            name=name,
            email=uemail,
            phone=phone,
            qty=qty,
            price_at_order=product.price * qty,
            pname=product.name
        )
        total += product.price * qty
        db.session.add(uorder)
    db.session.commit()
    
    session["order_success"] = True
    session["order_name"] = name
    session["order_total"] = total
    
    return redirect(url_for('purchase_route.order_success'))

@purchase_bp.route('/order-success')
def order_success():
    
    if not session.get("order_success"):
        return redirect(url_for("home_route.home"))
    
    name = session.get('order_name')
    total = session.get('order_total')
    
    session.pop("order_success", None)
    session.pop("order_name", None)
    session.pop("order_total", None)
    
    return render_template('order_confirm.html', name=name, total=total)

@purchase_bp.context_processor
def inject_fav_count():
    if 'user' in session:
        email = session.get('user')
        fav_count = Favourite.query\
            .filter_by(user_email=email)\
                .count()
        return dict(fav_count=fav_count)
    return dict(fav_count=0)

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