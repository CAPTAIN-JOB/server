from app import create_app, db
from models import *
from datetime import datetime, timedelta


app = create_app()

with app.app_context():
    # Drop all tables and recreate them 
    db.drop_all()
    db.create_all()

    # Seed Users
    users = [
        User(name="Alice Johnson", username="alice", email="alice@gmail.com", password="password123"),
        User(name="Bob Smith", username="bob", email="bob@gmail.com", password="password345"),
        User(name="Charlie Brown", username="charlie", email="charlie@gmail.com", password="password678"),
    ]
    db.session.add_all(users)
    db.session.commit()

    print(f"Seeded {len(users)} users.")

    # Seed Diseases
    diseases = [
        Disease(
            name="Malaria",
            description="A disease caused by a plasmodium parasite, transmitted by the bite of infected mosquitoes.",
            symptoms="Fever, chills, sweating, headaches.",
            prevention_tips="Use mosquito nets, insect repellents, and take antimalarial drugs.",
        ),
        Disease(
            name="COVID-19",
            description="A contagious disease caused by the SARS-CoV-2 virus.",
            symptoms="Fever, cough, fatigue, loss of taste or smell.",
            prevention_tips="Wear masks, maintain social distance, and get vaccinated.",
        ),
        Disease(
            name="Diabetes",
            description="A chronic condition characterized by high blood sugar levels.",
            symptoms="Increased thirst, frequent urination, fatigue.",
            prevention_tips="Maintain a healthy diet, exercise regularly, monitor blood sugar levels.",
        ),
    ]
    db.session.add_all(diseases)
    db.session.commit()

    print(f"Seeded {len(diseases)} diseases.")

    # Seed Events
    events = [
        Event(
            title="Health Awareness Seminar",
            description="A seminar to discuss and spread awareness about common health issues.",
            date=datetime.now() + timedelta(days=5),
            banner="https://plus.unsplash.com/premium_photo-1705267936105-90b76568cb17?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fGhlYWx0aCUyMGF3YXJlbmVzcyUyMHNlbWluYXJ8ZW58MHx8MHx8fDA%3D",
            created_by_user_id=1,
        ),
        Event(
            title="Malaria Prevention Workshop",
            description="A workshop to educate people about malaria prevention techniques.",
            date=datetime.now() + timedelta(days=10),
            banner="https://media.istockphoto.com/id/1326646787/photo/doctors-explaining-telemedicine-to-patient-in-rural-area.webp?a=1&b=1&s=612x612&w=0&k=20&c=wf6zeU-LthsKgC2nn2peTtU1FemNaufDZNBv0BlkZdM=",
            created_by_user_id=2,
        ),
        Event(
            title="COVID-19 Vaccination Drive",
            description="A community vaccination drive to combat the spread of COVID-19.",
            date=datetime.now() + timedelta(days=15),
            banner="https://plus.unsplash.com/premium_photo-1661515590895-e2f4d9d16fbb?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y292aWQlMjB2YWNjaW5hdGlvbiUyMGRyaXZlfGVufDB8fDB8fHww",
            created_by_user_id=3,
        ),
    ]
    db.session.add_all(events)
    db.session.commit()

    print(f"Seeded {len(events)} events.")

    print("Seeding completed!")
