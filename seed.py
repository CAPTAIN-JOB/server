from datetime import datetime

from app import create_app
from extensions import db
from models import *

app = create_app()


def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(Map).delete()
        db.session.query(AffectedArea).delete()
        db.session.query(Transaction).delete()
        db.session.query(Pay).delete()
        db.session.query(Event).delete()
        db.session.query(Role).delete()
        db.session.query(User).delete()
        db.session.query(Disease).delete()

        # Create users
        admin_user = User(
            name="Admin User", username="admin", email="admin@example.com"
        )
        admin_user.set_password("adminpass")
        user1 = User(name="John Doe", username="johndoe", email="johndoe@example.com")
        user1.set_password("password123")
        user2 = User(name="Jane Doe", username="janedoe", email="janedoe@example.com")
        user2.set_password("password456")
        db.session.add_all([admin_user, user1, user2])
        db.session.commit()

        # Create roles
        admin_role = Role(name="Admin", slug="admin")
        user_role = Role(name="User", slug="user")
        db.session.add_all([admin_role, user_role])
        db.session.commit()

        # Assign roles to users
        admin_user.roles.append(admin_role)
        user1.roles.append(user_role)
        user2.roles.append(user_role)
        db.session.commit()

        # Create events
        event1 = Event(
            title="Health Workshop",
            description="A workshop on health tips.",
            date=datetime(2024, 12, 15, 10, 0),
            banner="workshop.jpg",
            created_by_user_id=admin_user.id,
        )
        event2 = Event(
            title="Charity Run",
            description="A fundraising run event.",
            date=datetime(2024, 12, 20, 8, 30),
            banner="run.jpg",
            created_by_user_id=user1.id,
        )
        db.session.add_all([event1, event2])
        db.session.commit()

        # Create diseases
        disease1 = Disease(
            name="Diabetes",
            description="A chronic disease that affects how the body processes blood sugar.",
            symptoms="Increased thirst, frequent urination, extreme hunger.",
            prevention_tips="Maintain a healthy weight, eat balanced meals, exercise regularly.",
        )
        disease2 = Disease(
            name="Hypertension",
            description="A condition in which the blood pressure is consistently too high.",
            symptoms="Headaches, shortness of breath, nosebleeds.",
            prevention_tips="Reduce salt intake, exercise, avoid stress.",
        )
        db.session.add_all([disease1, disease2])
        db.session.commit()

        # Create payments
        payment1 = Pay(
            transaction_id="TXN12345",
            amount=100.50,
            phone_number="254700123456",
            status="Completed",
        )
        payment2 = Pay(
            transaction_id="TXN12346",
            amount=200.75,
            phone_number="254711123456",
            status="Pending",
        )
        db.session.add_all([payment1, payment2])
        db.session.commit()

        # Create transactions
        transaction1 = Transaction(
            transaction_id="TRX001",
            phone_number="254700123456",
            amount=100.50,
            status="Completed",
        )
        transaction2 = Transaction(
            transaction_id="TRX002",
            phone_number="254711123456",
            amount=200.75,
            status="Pending",
        )
        db.session.add_all([transaction1, transaction2])
        db.session.commit()

        # Create affected areas
        area1 = AffectedArea(
            name="Nairobi",
            location="Kenya",
            latitude=-1.286389,
            longitude=36.817223,
            disease_count=5,
        )
        area2 = AffectedArea(
            name="Mombasa",
            location="Kenya",
            latitude=-4.043477,
            longitude=39.668207,
            disease_count=2,
        )
        db.session.add_all([area1, area2])
        db.session.commit()

        # Create maps
        map1 = Map(
            affected_area_id=area1.id, map_data={"type": "Feature", "geometry": {}}
        )
        map2 = Map(
            affected_area_id=area2.id, map_data={"type": "Feature", "geometry": {}}
        )
        db.session.add_all([map1, map2])
        db.session.commit()

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
