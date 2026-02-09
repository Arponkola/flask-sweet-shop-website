from .login_route import login_bp
from .home_route import home_bp
from .register_route import register_bp
from .search_route import search_bp
from .favourite_route import fav_bp
from .purchase_route import purchase_bp
from .admin_route import admin_bp
from .admin_sweet_route import admin_sweet_bp
from .admin_order_route import admin_order_bp


blueprints = {
    home_bp : "/", 
    login_bp : "/",
    register_bp : "/",
    search_bp : "/",
    fav_bp : "/",
    purchase_bp: "/",
    admin_bp : "/",
    admin_sweet_bp:"/admin",
    admin_order_bp: "/admin"
}