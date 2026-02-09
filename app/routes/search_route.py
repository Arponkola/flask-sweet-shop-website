import flask
from flask import request, render_template, Blueprint, redirect, url_for, session
from app.model.products import Product
from app.model.fav import Favourite

search_bp = Blueprint(
        "search_route",
        __name__,
        static_folder='static',
        template_folder='templates'
    )

@search_bp.route('/search/')
def search():
    
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('home_route.home'))
    
    products = Product.query.filter(
        Product.is_active == True,
        Product.name.ilike(f"%{query}%")
    ).all()
    
    fav_ids = []
    if 'user' in session:
        email = session['user']
        fav_ids = [f.product_id for f in Favourite.query.filter_by(user_email=email).all()]
    
    
    return render_template(
        "search.html", 
        products=products,
        query=query,
        fav_ids=fav_ids
        ) #render html content of registation page

@search_bp.context_processor
def inject_fav_count():
    if 'user' in session:
        email = session.get('user')
        fav_count = Favourite.query\
            .filter_by(user_email=email)\
                .count()
        return dict(fav_count=fav_count)
    return dict(fav_count=0)
