from flask import Blueprint, render_template, session, redirect, url_for, request
from functools import wraps
from app.extension import db
from app.model.order import Orders
from app.model.products import Product
from app.model.fav import Favourite
from sqlalchemy.exc import SQLAlchemyError
import pytz

admin_order_bp = Blueprint(
    "admin_order_route", __name__,
    template_folder="templates",
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

@admin_order_bp.context_processor
def inject_fav_count():
    if 'user' in session:
        email = session.get('user')
        fav_count = Favourite.query\
            .filter_by(user_email=email)\
                .count()
        return dict(fav_count=fav_count)
    return dict(fav_count=0)


@admin_order_bp.route('/orders', methods=['GET', 'POST'])
@admin_required
def orders():
    ords = Orders.query.all()
    
    pending_orders = []
    for pord in ords:
        if pord.status == "pending":
            pending_orders.append(pord)
    
    return render_template("admin_orders.html", orders=pending_orders)

@admin_order_bp.route('/orders/delete/<int:order_id>', methods=["GET", "POST"])
@admin_required
def order_delete(order_id:int):
    order = Orders.query.get(order_id)
    if order and order.status == "pending":
        try:
            db.session.delete(order)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for('admin_order_route.orders'))

@admin_order_bp.route('/orders/placed/<int:order_id>', methods=["GET", "POST"])
@admin_required
def order_placed(order_id: int):
    try:
        order = Orders.query.get(order_id)
        if not order:
            return redirect(url_for(
                "admin_order_route.orders",
                error="Order not found"
            ))

        product = Product.query.get(order.product_id)
        if not product:
            return redirect(url_for(
                "admin_order_route.orders",
                error="Product not found"
            ))

        remaining_qty = product.stock - order.qty

        if remaining_qty < 0:
            return redirect(url_for(
                "admin_order_route.orders",
                error="Order quantity is greater than available stock"
            ))

        # Update product stock
        product.stock = remaining_qty

        if remaining_qty == 0:
            product.is_active = False

        # Update order status
        order.status = "placed"

        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        print("DB ERROR:", e)  # replace with logging in production
        return redirect(url_for(
            "admin_order_route.orders",
            error="Something went wrong while placing the order"
        ))

    return redirect(url_for("admin_order_route.orders"))

    

@admin_order_bp.route('/orders/history', methods=["GET"])
@admin_required
def order_history():
    order = Orders.query.filter_by(status="placed").all()
    return render_template("order_history.html", orders=order)

@admin_order_bp.route('/orders/history/delete/<int:order_id>', methods=["GET", "POST"])
@admin_required
def order_history_delete(order_id:int):
    order = Orders.query.get(order_id)
    if order and order.status == "placed":
        try:
            db.session.delete(order)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect(url_for("admin_order_route.order_history"))