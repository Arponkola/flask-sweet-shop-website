from app.extension import db

class LoginUsers(db.Model):
    __tablename__ = "login_users"

    userId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    favourites = db.relationship(
        "Favourite",          # STRING name
        backref="user",
        cascade="all, delete-orphan"
    )

    def to_json(self):
        return {
            "userId": self.userId,
            "name": self.name,
            "email": self.email,
            "mobileNumber": self.mobile_number
        }

def create_login_table(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def add_login_details(name:str, email:str, password:str, mobile_number:int, is_admin:bool=False):
    user = LoginUsers(
        name = name,
        email = email,
        password = password,
        mobile_number = mobile_number,
        is_admin = is_admin
    )
    
    db.session.add(user)
    db.session.commit()

def search_from_login_user(uemail:str):
    user = LoginUsers.query.filter_by(email=uemail).first()
    return user