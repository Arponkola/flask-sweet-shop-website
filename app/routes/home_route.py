from flask import render_template, Blueprint, session
from app.model.products import Product
from app.model.fav import Favourite

home_bp = Blueprint("home_route", __name__, template_folder="templates", static_folder="static")

@home_bp.route("/")
def home():
    products = Product.query.filter_by(is_active=True).all()
    fav_ids = []
    for fid in Favourite.query.filter_by(user_email=session.get('user')).all():
        fav_ids.append(fid.product_id)
    
    return render_template("homepage.html", session=session, products=products, fav_ids=fav_ids)

@home_bp.context_processor
def inject_fav_count():
    if 'user' in session:
        email = session.get('user')
        fav_count = Favourite.query\
            .filter_by(user_email=email)\
                .count()
        return dict(fav_count=fav_count)
    return dict(fav_count=0)