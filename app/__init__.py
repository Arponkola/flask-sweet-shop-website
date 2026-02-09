from flask import Flask
from .extension import db, bcrypt, format_ist
from app.routes import blueprints
from app.model.user import create_login_table
from app.model.products import create_product_table
from app.model.fav import create_fav_table
from app.model.order import create_order_table
import os


def create_app()->Flask:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    IMAGE_FOLDER = os.path.join(BASE_DIR, "static", "images")
    
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    print(app.config["SECRET_KEY"])
    
    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # Render fix
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://", "postgresql://", 1
            )
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        
    else:
        data_folder = os.path.join(BASE_DIR, 'data')
        os.makedirs(data_folder, exist_ok=True)
        DB_PATH = os.path.join(data_folder, 'sweet.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["IMAGE_FOLDER"] = IMAGE_FOLDER
    app.jinja_env.filters["ist"] = format_ist
    
    create_login_table(app)
    create_product_table(app)
    create_fav_table(app)
    create_order_table(app)
    
    bcrypt.init_app(app)
    
    for name in blueprints.keys():
        app.register_blueprint(name, url_prefix=blueprints[name])
    
    return app
