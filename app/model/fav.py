from app.extension import db

class Favourite(db.Model):
    __tablename__ = "favourites"

    id = db.Column(db.Integer, primary_key=True)

    user_email = db.Column(
        db.String(100),
        db.ForeignKey("login_users.email"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint("user_email", "product_id", name="unique_favourite"),
    )

def create_fav_table(app):
    with app.app_context():
        db.create_all()