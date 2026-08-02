# Good Heart Children's Home

A Flask website and admin dashboard for Good Heart Children's Home.

## Features

- Public pages: Home, About Us, Mission, Vision, Programs, Team, Gallery, News & Events, Volunteer, Donate, Contact
- Admin dashboard with management screens for children, staff, volunteers, donations, gallery, blog/news, events, messages, reports, and users
- SQLAlchemy models for all requested tables
- Flask-Login authentication
- Flask-WTF forms and CSRF protection
- SQLite for development and PostgreSQL-ready configuration for production

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=mynameissecretofscrets
DATABASE_URL=sqlite:///instance/good_heart.db
```

Run the app:

```bash
python run.py
```

Open `http://127.0.0.1:5000`.

## Create the First Admin User

Run this from the project folder:

```bash
flask --app run shell
```

Then paste:

```python
from app import app, db
from app.models import User

with app.app_context():
    user = User(
        name="Administrator",
        email="admin@goodheart.local",
        role="admin"
    )
    user.set_password("ChangeMe123!")

    db.session.add(user)
    db.session.commit()

    print("Admin user created successfully.")
```

Log in at `/login` and change the password by editing the user in the admin area.

## Production Notes

- Set `SECRET_KEY` to a secure value.
- Set `DATABASE_URL` to your PostgreSQL connection string.
- Use Gunicorn behind Nginx:

```bash
gunicorn "run:app"
```

Future integrations can be added for M-Pesa, PayPal, email notifications, sponsorships, event registration, newsletter subscriptions, and PDF receipts.
