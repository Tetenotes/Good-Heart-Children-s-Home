from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    EmailField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

# login form for admin users
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")

# contact form for the website
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    subject = StringField("Subject", validators=[DataRequired(), Length(max=160)])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send message")

# volunteer form for the website
class VolunteerForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=40)])
    skills = StringField("Skills", validators=[Optional(), Length(max=255)])
    availability = StringField("Availability", validators=[Optional(), Length(max=120)])
    submit = SubmitField("Apply to volunteer")

# donation form for the website
class DonationForm(FlaskForm):
    donor_name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    email = EmailField("Email", validators=[Optional(), Email()])
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=1)])
    currency = SelectField("Currency", choices=[("KES", "KES"), ("USD", "USD")])
    method = SelectField(
        "Method",
        choices=[("Manual", "Manual pledge"), ("M-Pesa", "M-Pesa"), ("PayPal", "PayPal")],
    )
    message = TextAreaField("Message", validators=[Optional()])
    submit = SubmitField("Record pledge")

# forms for the admin dashboard
class ChildForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=25)])
    gender = StringField("Gender", validators=[Optional(), Length(max=20)])
    health_status = StringField("Health status", validators=[Optional(), Length(max=160)])
    education_level = StringField("Education level", validators=[Optional(), Length(max=120)])
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Save child")

# staff form for the admin dashboard
class StaffForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(max=120)])
    position = StringField("Position", validators=[DataRequired(), Length(max=120)])
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    email = EmailField("Email", validators=[Optional(), Email()])
    bio = TextAreaField("Bio", validators=[Optional()])
    photo_url = StringField("Photo URL", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Save staff")

# gallery form for the admin dashboard
class GalleryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=160)])
    image_url = StringField("Image URL", validators=[DataRequired(), Length(max=255)])
    caption = TextAreaField("Caption", validators=[Optional()])
    is_featured = BooleanField("Featured")
    submit = SubmitField("Save gallery item")

# news form for the admin dashboard
class NewsForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=180)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=200)])
    summary = StringField("Summary", validators=[Optional(), Length(max=255)])
    body = TextAreaField("Body", validators=[DataRequired()])
    published = BooleanField("Published", default=True)
    submit = SubmitField("Save post")

# event form for the admin dashboard
class EventForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=160)])
    event_date = DateField("Event date", validators=[Optional()])
    location = StringField("Location", validators=[Optional(), Length(max=160)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Save event")

# user form for the admin dashboard
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Optional(), Length(min=8)])
    role = SelectField("Role", choices=[("admin", "Admin"), ("editor", "Editor")])
    is_active_admin = BooleanField("Active", default=True)
    submit = SubmitField("Save user")
