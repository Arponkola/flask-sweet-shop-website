from flask import Blueprint, render_template, session, redirect, url_for, request, current_app
from functools import wraps
from app.extension import db
from app.model.products import Product
from app.model.fav import Favourite
import os, uuid

admin_sweet_bp = Blueprint(
    "admin_sweet_route", __name__,
    template_folder="template",
    static_folder="static"
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

@admin_sweet_bp.route('/sweets', methods=['GET', 'POST'])
@admin_required
def all_sweets():
    sweets = Product.query.all()
    return render_template("admin_sweets.html", sweets=sweets)

@admin_sweet_bp.route('/sweets/add', methods=['GET', 'POST'])
@admin_required
def add_sweet():
    if request.method == "POST":
        image_file = request.files.get("image")
        name = request.form.get("name")
        price = request.form.get("price")
        stock = request.form.get("stock")
        
        valid_format = ("png", "jpg", "jpeg")
        
        if image_file.filename == "":
            return render_template("sweet_form.html", error="Not a Valid File name")
        
        if not image_file.filename.endswith(valid_format):
            return render_template("sweet_form.html", error="Not a Valid Format")
        
        ext = os.path.splitext(image_file.filename)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        
        
        save_path = os.path.join(current_app.config["IMAGE_FOLDER"], filename)
        image_file.save(save_path)
        
        product = Product(
            name=name,
            price=price,
            image=filename,
            stock=stock
        )
        
        try:
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        finally:
            return redirect(url_for("admin_sweet_route.all_sweets"))
    return render_template("sweet_form.html")

@admin_sweet_bp.route('/sweets/update/<int:sweet_id>', methods=['GET', 'POST'])
@admin_required
def update_sweet(sweet_id):
    if request.method == "POST":
        sweet = Product.query.get(sweet_id)
        
        image_file = request.files.get("image")
        name = request.form.get("name", sweet.name, type=str)
        price = request.form.get("price", sweet.price, type=float)
        stock = request.form.get("stock", sweet.stock, type=int)
        is_active = request.form.get("is_active", type=str)
        
        
        if not sweet_id:
            return render_template("update_sweet_form.html", sweet_details=sweet, error="Sweet Id Must Be Some Number Not Empty")
        
        valid_format = ("png", "jpg", "jpeg")
        
        sweet.name = name
        sweet.price = price
        sweet.is_active = 1 if is_active in ["yes", "Yes", "yEs", "YES", "YeS", "Yes", "1"] else 0
        sweet.stock = stock
        
        if image_file.filename=="":
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            finally:
                return redirect(url_for("admin_sweet_route.all_sweets"))
        
        if image_file.filename.endswith(valid_format):
            ext = os.path.splitext(image_file.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
        
            save_path = os.path.join(current_app.config["IMAGE_FOLDER"], filename)
            image_file.save(save_path)
            sweet.image = filename
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
            finally:
                return redirect(url_for("admin_sweet_route.all_sweets"))
        
        return render_template("update_sweet_form.html", sweet_details=sweet, error="File Format Not Allowed")
    
    sweet_details = Product.query.get(sweet_id)
    if not sweet_details:
        return render_template("update_sweet_form.html", error="Sweet ID Is Not Present In Valid Sweet Id")
        
    return render_template("update_sweet_form.html", sweet_details=sweet_details)



@admin_sweet_bp.route('/sweets/delete/<int:sweet_id>', methods=['GET', 'POST'])
@admin_required
def delete_sweet(sweet_id):
    product = Product.query.get(sweet_id)
    if not product:
        return "Select a Valid Product"
    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        pass
    return redirect(url_for("admin_sweet_route.all_sweets"))

@admin_sweet_bp.context_processor
def inject_fav_count():
    if 'user' in session:
        email = session.get('user')
        fav_count = Favourite.query\
            .filter_by(user_email=email)\
                .count()
        return dict(fav_count=fav_count)
    return dict(fav_count=0)
