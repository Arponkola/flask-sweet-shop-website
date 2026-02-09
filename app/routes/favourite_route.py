from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from app.model.fav import Favourite
from app.model.products import Product
from app.extension import db
from sqlalchemy.exc import IntegrityError

fav_bp = Blueprint("favourite_route", __name__,
    template_folder="templates",
    static_folder="static")

@fav_bp.route('/favourite', methods=['GET', 'POST'])
def favourite():
    if 'user' in session:
        email = session.get('user')
        items = (
        db.session.query(Product.id, Product.name, Product.price, Product.image)
            .join(Favourite)
            .filter(Favourite.user_email == email)
            .all()
        )
        
        return render_template("favourite.html", sweets=items)
    
    return redirect(url_for("login_route.login"))

@fav_bp.context_processor
def inject_fav_count():
    if 'user' in session:
        email = session.get('user')
        fav_count = Favourite.query\
            .filter_by(user_email=email)\
                .count()
        return dict(fav_count=fav_count)
    return dict(fav_count=0)

@fav_bp.route("/add-to-favourite/<int:product_id>", methods=["POST"])
def add_to_favourite(product_id):    
    email = session.get("user")
    if not email:
        return jsonify(success=False, redirect=True), 401

    # Check if already favourited
    fav = Favourite.query.filter_by(
            user_email=email,
            product_id=product_id
        ).first()
        

    if fav:
        # Already favourited → remove
        try:
            db.session.delete(fav)
            db.session.commit()
            action = "removed"
        except IntegrityError:
            db.session.rollback()
    else:
        # Not favourited → add
        
        try:
            fav = Favourite(user_email=email, product_id=product_id)
            db.session.add(fav)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        action = "added"

    # Get updated favourite count
    count = Favourite.query.filter_by(user_email=email).count()

    return jsonify(success=True, action=action, count=count)