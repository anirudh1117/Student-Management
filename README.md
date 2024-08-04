# Student Management System

Welcome to the Student Management System repository! This project is designed to simplify the administration of student data for educational institutions. It features functionalities that allow users to manage student profiles, track academic progress, and more.

## Features

- **Manage Student Profiles**: Add, update, and delete student profiles including personal details and educational backgrounds.
- **Track Academic Progress**: Monitor and record students' academic performances and progress reports.
- **User Authentication**: Secure login system for administrators and students.
- **Responsive Design**: Accessible on various devices, ensuring a seamless user experience.

## Built With

- **Django**: For robust back-end functionality.
- **SQLite**: Used for the database to store student and system data.
- **Bootstrap**: For responsive front-end design.
- **Python**: The main programming language used.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

```bash
git clone https://github.com/anirudh1117/Student-Management.git

cd Student-Management

python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver


