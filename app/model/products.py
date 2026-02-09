from app.extension import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))
    category = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    favourites = db.relationship(
        "Favourite",
        backref="product",
        cascade="all, delete-orphan"
    )
    
    orders = db.relationship(
        "Orders",
        backref="product",
        cascade="all, delete-orphan"
    )
   
def create_product_table(app):
    with app.app_context():
        db.create_all()