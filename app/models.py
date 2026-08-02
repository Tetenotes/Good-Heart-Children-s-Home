from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager

# user loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# mixin class to add created_at and updated_at timestamps to models
class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

# models for the application
class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default="admin", nullable=False)
    is_active_admin = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# child model for the application
class Child(TimestampMixin, db.Model):
    __tablename__ = "children"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    health_status = db.Column(db.String(160))
    education_level = db.Column(db.String(120))
    notes = db.Column(db.Text)


class Staff(TimestampMixin, db.Model):
    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40))
    email = db.Column(db.String(160))
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))


class Volunteer(TimestampMixin, db.Model):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    skills = db.Column(db.String(255))
    availability = db.Column(db.String(120))
    status = db.Column(db.String(30), default="New", nullable=False)


class Donation(TimestampMixin, db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160))
    phone = db.Column(db.String(40))
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(10), default="KES", nullable=False)
    method = db.Column(db.String(60), default="Manual", nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(30), default="Pending", nullable=False)


class GalleryItem(TimestampMixin, db.Model):
    __tablename__ = "gallery"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)


class Event(TimestampMixin, db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    event_date = db.Column(db.Date)
    location = db.Column(db.String(160))
    description = db.Column(db.Text)


class News(TimestampMixin, db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    summary = db.Column(db.String(255))
    body = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=True, nullable=False)


class ContactMessage(TimestampMixin, db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(40))
    subject = db.Column(db.String(160), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
