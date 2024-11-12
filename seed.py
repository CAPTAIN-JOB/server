# seed.py
from app import create_app  # Import the app factory function
from extensions import db  # Import db from extensions.py
from models import Event, Disease, Pay  # Import the models
from datetime import datetime

app = create_app()  # Create an app instance

def seed_data():
    with app.app_context():  # Set up the application context
        # Clear existing data
        db.session.query(Event).delete()
        db.session.query(Disease).delete()
        db.session.query(Pay).delete()
        
        # Seed Event data
        events = [
            Event(
                title="Health Awareness Workshop",
                description="A workshop to educate about healthy living.",
                date=datetime(2024, 12, 15, 10, 0),
                banner="banner1.jpg",
                created_by_user_id=1
            ),
            Event(
                title="Charity Run for NCDs",
                description="Fundraising event to support NCD patients.",
                date=datetime(2024, 12, 20, 8, 30),
                banner="banner2.jpg",
                created_by_user_id=2
            ),
        ]

        # Seed Disease data
        diseases = [
            Disease(
                name="Diabetes",
                description="A chronic condition that affects blood sugar regulation.",
                symptoms="Increased thirst, frequent urination, fatigue.",
                prevention_tips="Maintain a healthy diet, exercise regularly, monitor blood sugar levels."
            ),
            Disease(
                name="Hypertension",
                description="High blood pressure often with no noticeable symptoms.",
                symptoms="Headaches, shortness of breath, nosebleeds.",
                prevention_tips="Reduce salt intake, exercise, avoid excessive alcohol."
            ),
        ]

        # Seed Pay data
        payments = [
            Pay(
                transaction_id="TX123456789",
                amount=150.0,
                phone_number="254712345678",
                status="Completed"
            ),
            Pay(
                transaction_id="TX987654321",
                amount=300.0,
                phone_number="254723456789",
                status="Pending"
            ),
        ]

        # Add data to session and commit
        db.session.bulk_save_objects(events)
        db.session.bulk_save_objects(diseases)
        db.session.bulk_save_objects(payments)
        db.session.commit()
        print("Data seeded successfully.")

if __name__ == "__main__":
    seed_data()
