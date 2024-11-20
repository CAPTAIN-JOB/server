Non-Communicable Diseases Charity - Backend
This repository contains the backend implementation for Project: Non-Communicable Diseases Charity. It is built using Python (Flask) and is responsible for managing APIs, database operations, and business logic for the application.

Table of Contents
Introduction
Features
Tech Stack
Setup and Installation
Environment Variables
Database Schema
API Endpoints
Testing
License
Introduction
The backend serves as the foundation for the Project 24 platform, supporting user account management, communicable disease records, affected areas, and donation tracking. It also provides an admin panel for managing users and content.

Features
User Features
Account registration and login with JWT-based authentication.
View a list of the most prevalent communicable diseases.
Access detailed information about diseases and affected areas.
Provide reviews on how to contribute to eradicating diseases.
View geographic maps for disease analysis in specific regions.
Donate to affected areas.
Admin Features
Manage users, including creating new accounts and modifying roles.
Perform CRUD operations for communicable disease records.
Perform CRUD operations for affected area records.
Tech Stack
Core Technologies
Backend Framework: Python (Flask)
Database: PostgreSQL
Authentication: JWT (JSON Web Token)
Testing Framework: Minitests
Setup and Installation
Prerequisites
Python 3.9+
PostgreSQL
Virtualenv (optional but recommended)
Steps
Clone the Repository:

bash
Copy code
git clone https://github.com/username/project24-backend.git  
cd project24-backend  
Create and Activate a Virtual Environment:

bash
Copy code
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
Install Dependencies:

bash
Copy code
pip install -r requirements.txt  
Set Up the Database:

Ensure PostgreSQL is running.
Create a new database:
sql
Copy code
CREATE DATABASE project24_db;  
Run Database Migrations:

bash
Copy code
flask db upgrade  
Start the Development Server:

bash
Copy code
flask run  
The API should now be accessible at http://127.0.0.1:5000.

Environment Variables
Create a .env file in the project root and add the following:

env
Copy code
FLASK_ENV=development  
SECRET_KEY=your_secret_key  
DATABASE_URL=postgresql://username:password@localhost:5432/project24_db  
JWT_SECRET_KEY=your_jwt_secret_key  
Database Schema
The database schema includes the following primary tables:

Users: Stores user information (e.g., name, email, role).
Diseases: Records information about communicable diseases.
AffectedAreas: Stores details of regions impacted by diseases.
Donations: Tracks user contributions to affected areas.
Reviews: Captures user feedback and suggestions.
API Endpoints
Authentication
POST /api/auth/register: Register a new user.
POST /api/auth/login: Login and obtain a JWT token.
Diseases
GET /api/diseases: Retrieve a list of diseases.
POST /api/diseases (Admin): Create a new disease entry.
Affected Areas
GET /api/areas: Retrieve affected areas.
POST /api/areas (Admin): Add a new affected area.
Donations
POST /api/donations: Make a donation.
Reviews
POST /api/reviews: Submit a review for an affected area.
Testing
Run tests with the following command:

bash
Copy code
pytest tests/  
Code Coverage
Ensure your code is thoroughly tested. Generate a coverage report using:

bash
Copy code
pytest --cov=app  
License
This project is licensed under the MIT License. See the LICENSE file for details.