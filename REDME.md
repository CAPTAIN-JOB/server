# Non-Communicable Diseases Charity - Backend

This repository contains the backend implementation for Project: Non-Communicable Diseases Charity. It is built using Python (Flask) and is responsible for managing APIs, database operations, and business logic for the application.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
    - [User Features](#user-features)
    - [Admin Features](#admin-features)
3. [Tech Stack](#tech-stack)
4. [Setup and Installation](#setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
5. [Environment Variables](#environment-variables)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)
8. [Testing](#testing)
9. [License](#license)

## Introduction

The backend serves as the foundation for the Project 24 platform, supporting user account management, communicable disease records, affected areas, and donation tracking. It also provides an admin panel for managing users and content.

## Features

### User Features
- Account registration and login with JWT-based authentication.
- View a list of the most prevalent communicable diseases.
- Access detailed information about diseases and affected areas.
- Provide reviews on how to contribute to eradicating diseases.
- View geographic maps for disease analysis in specific regions.
- Donate to affected areas.

### Admin Features
- Manage users, including creating new accounts and modifying roles.
- Perform CRUD operations for communicable disease records.
- Perform CRUD operations for affected area records.

## Tech Stack

### Core Technologies
- **Backend Framework**: Python (Flask)
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Token)
- **Testing Framework**: Minitests

## Setup and Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Virtualenv (optional but recommended)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/project24-backend.git  
   cd project24-backend
