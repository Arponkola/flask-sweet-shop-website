# extensions.py
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import pytz
from datetime import timezone

def format_ist(dt):
    if not dt:
        return ""

    # FORCE UTC if DB returned naive datetime
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    ist = pytz.timezone("Asia/Kolkata")
    dt_ist = dt.astimezone(ist)

    return dt_ist.strftime("%d %b %Y, %I:%M %p")


bcrypt = Bcrypt()
db = SQLAlchemy()