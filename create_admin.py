from app import create_app, db
from app.models import User

app = create_app()

admins = [
    {
        "name": "Administrator One",
        "email": "admin1@gmail.com",
        "password": "Admin123!"
    },
    {
        "name": "Administrator Two",
        "email": "admin2@gmail.com",
        "password": "Admin123!"
    },
    {
        "name": "Administrator Three",
        "email": "admin3@gmail.com",
        "password": "Admin123!"
    }
]

with app.app_context():
    for admin_data in admins:
        existing = User.query.filter_by(email=admin_data["email"]).first()

        if existing:
            print(f"{admin_data['email']} already exists.")
            continue

        user = User(
            name=admin_data["name"],
            email=admin_data["email"],
            role="admin"
        )
        user.set_password(admin_data["password"])

        db.session.add(user)

    db.session.commit()
    print("Admin accounts created successfully!")