from app.extension import db
from datetime import datetime, timezone

class Orders(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(15), nullable=False)
    pname = db.Column(db.String(50), nullable=False)

    qty = db.Column(db.Integer, nullable=False, default=1)

    price_at_order = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(
        db.String(20),
        default="pending"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    def __repr__(self):
        return f"<Order {self.id} | {self.email}>"

def create_order_table(app):
    with app.app_context():
        db.create_all()