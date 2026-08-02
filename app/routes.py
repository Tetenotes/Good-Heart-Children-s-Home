from datetime import datetime
from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.forms import (
    ChildForm,
    ContactForm,
    DonationForm,
    EventForm,
    GalleryForm,
    NewsForm,
    StaffForm,
    UserForm,
    VolunteerForm,
)
from app.models import (
    Child,
    ContactMessage,
    Donation,
    Event,
    GalleryItem,
    News,
    Staff,
    User,
    Volunteer,
)

main_bp = Blueprint("main", __name__)

# contact information to be injected into templates
CONTACT = {
    "name": "Good Heart Children's Home",
    "phones": ["+254 711 812 012", "+254 791 721 398"],
    "email": "goodheart.org12@gmail.com",
}

# context processor to inject contact information and current year into templates
@main_bp.app_context_processor
def inject_contact():
    return {"contact_info": CONTACT, "current_year": datetime.utcnow().year}

# decorator to restrict access to admin users
def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_active_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped

# route for the home page
@main_bp.route("/")
def home():
    gallery = GalleryItem.query.filter_by(is_featured=True).order_by(GalleryItem.created_at.desc()).limit(6).all()
    news_items = News.query.filter_by(published=True).order_by(News.created_at.desc()).limit(3).all()
    events = Event.query.order_by(Event.event_date.desc().nullslast()).limit(3).all()
    return render_template("home.html", gallery=gallery, news_items=news_items, events=events, title="Home")

# route for the about us page
@main_bp.route("/about-us")
def about():
    staff = Staff.query.order_by(Staff.full_name).all()
    return render_template("about.html", staff=staff, title="About Us")

# route for the mission page
@main_bp.route("/our-mission")
def mission():
    return render_template("mission.html", title="Our Mission")

# route for the vision page
@main_bp.route("/our-vision")
def vision():
    return render_template("vision.html", title="Our Vision")

# route for the programs page
@main_bp.route("/our-programs")
def programs():
    return render_template("programs.html", title="Our Programs")

# route for the team page
@main_bp.route("/meet-our-team")
def team():
    staff = Staff.query.order_by(Staff.full_name).all()
    return render_template("team.html", staff=staff, title="Meet Our Team")

# route for the gallery page
@main_bp.route("/gallery")
def gallery():
    items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).all()
    return render_template("gallery.html", items=items, title="Gallery")

# route for the news and events page
@main_bp.route("/news-events")
def news_events():
    posts = News.query.filter_by(published=True).order_by(News.created_at.desc()).all()
    events = Event.query.order_by(Event.event_date.desc().nullslast()).all()
    return render_template("news_events.html", posts=posts, events=events, title="News & Events")

# route for the volunteer page
@main_bp.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    form = VolunteerForm()
    if form.validate_on_submit():
        volunteer_record = Volunteer(
            full_name=form.full_name.data,
            email=form.email.data.lower(),
            phone=form.phone.data,
            skills=form.skills.data,
            availability=form.availability.data,
        )
        db.session.add(volunteer_record)
        db.session.commit()
        flash("Thank you for offering your time. Our team will contact you soon.", "success")
        return redirect(url_for("main.volunteer"))
    return render_template("volunteer.html", form=form, title="Volunteer")

# route for the donate page
@main_bp.route("/donate", methods=["GET", "POST"])
def donate():
    form = DonationForm()
    if form.validate_on_submit():
        donation = Donation(
            donor_name=form.donor_name.data,
            email=(form.email.data or "").lower() or None,
            phone=form.phone.data,
            amount=form.amount.data,
            currency=form.currency.data,
            method=form.method.data,
            message=form.message.data,
        )
        db.session.add(donation)
        db.session.commit()
        flash("Your donation pledge has been recorded. Thank you for caring.", "success")
        return redirect(url_for("main.donate"))
    return render_template("donate.html", form=form, title="Donate")

# route for the contact page
@main_bp.route("/contact-us", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data.lower(),
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data,
        )
        db.session.add(message)
        db.session.commit()
        flash("Your message has been sent. We will reply as soon as possible.", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form, title="Contact Us")

# admin dashboard routes
@main_bp.route("/admin")
@admin_required
def admin_dashboard():
    totals = {
        "children": Child.query.count(),
        "staff": Staff.query.count(),
        "volunteers": Volunteer.query.count(),
        "donations": Donation.query.count(),
        "messages": ContactMessage.query.filter_by(is_read=False).count(),
    }
    donation_total = db.session.query(func.coalesce(func.sum(Donation.amount), 0)).scalar()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        totals=totals,
        donation_total=donation_total,
        recent_messages=recent_messages,
        title="Admin Dashboard",
    )

# admin resource management routes
ADMIN_RESOURCES = {
    "children": (Child, ChildForm, "Manage Children", "full_name"),
    "staff": (Staff, StaffForm, "Manage Staff", "full_name"),
    "volunteers": (Volunteer, VolunteerForm, "Manage Volunteers", "full_name"),
    "donations": (Donation, DonationForm, "Manage Donations", "donor_name"),
    "gallery": (GalleryItem, GalleryForm, "Gallery Manager", "title"),
    "news": (News, NewsForm, "Blog Manager", "title"),
    "events": (Event, EventForm, "Events Manager", "title"),
    "users": (User, UserForm, "User Management", "name"),
}

# helper function to get the model, form class, label, and display field for a given resource
def get_resource(resource):
    if resource not in ADMIN_RESOURCES:
        abort(404)
    return ADMIN_RESOURCES[resource]

# manage admin resources: list, create, edit, delete
@main_bp.route("/admin/<resource>")
@admin_required
def admin_list(resource):
    model, form_class, label, display_field = get_resource(resource)
    records = model.query.order_by(model.created_at.desc()).all()
    return render_template(
        "admin/list.html",
        resource=resource,
        label=label,
        display_field=display_field,
        records=records,
        title=label,
    )

# 
@main_bp.route("/admin/<resource>/new", methods=["GET", "POST"])
@admin_required
def admin_create(resource):
    model, form_class, label, display_field = get_resource(resource)
    form = form_class()
    if form.validate_on_submit():
        if resource == "users" and not form.password.data:
            flash("Password is required when creating a new user.", "danger")
            return render_template("admin/form.html", form=form, label=label, action="Create", title=f"Create {label}")
        record = model()
        save_form_to_model(form, record)
        db.session.add(record)
        db.session.commit()
        flash(f"{label} record created.", "success")
        return redirect(url_for("main.admin_list", resource=resource))
    return render_template("admin/form.html", form=form, label=label, action="Create", title=f"Create {label}")


@main_bp.route("/admin/<resource>/<int:record_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_edit(resource, record_id):
    model, form_class, label, display_field = get_resource(resource)
    record = model.query.get_or_404(record_id)
    form = form_class(obj=record)
    if form.validate_on_submit():
        save_form_to_model(form, record)
        db.session.commit()
        flash(f"{label} record updated.", "success")
        return redirect(url_for("main.admin_list", resource=resource))
    return render_template("admin/form.html", form=form, label=label, action="Edit", title=f"Edit {label}")


@main_bp.route("/admin/<resource>/<int:record_id>/delete", methods=["POST"])
@admin_required
def admin_delete(resource, record_id):
    model, form_class, label, display_field = get_resource(resource)
    record = model.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    flash(f"{label} record deleted.", "info")
    return redirect(url_for("main.admin_list", resource=resource))


@main_bp.route("/admin/messages")
@admin_required
def admin_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages.html", messages=messages, title="Contact Messages")


@main_bp.route("/admin/messages/<int:message_id>/read", methods=["POST"])
@admin_required
def mark_message_read(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = True
    db.session.commit()
    flash("Message marked as read.", "success")
    return redirect(url_for("main.admin_messages"))


@main_bp.route("/admin/reports")
@admin_required
def reports():
    donation_total = db.session.query(func.coalesce(func.sum(Donation.amount), 0)).scalar()
    volunteer_count = Volunteer.query.count()
    child_count = Child.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    return render_template(
        "admin/reports.html",
        donation_total=donation_total,
        volunteer_count=volunteer_count,
        child_count=child_count,
        unread_messages=unread_messages,
        title="Reports",
    )


def save_form_to_model(form, record):
    for field_name, field in form._fields.items():
        if field_name in {"csrf_token", "submit"}:
            continue
        if field_name == "password":
            if field.data:
                record.set_password(field.data)
            continue
        if field_name == "email" and field.data:
            setattr(record, field_name, field.data.lower())
            continue
        setattr(record, field_name, field.data)
