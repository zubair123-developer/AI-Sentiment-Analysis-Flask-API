
# Task 1 - Student Management System

## Software Engineering Assignment 1

A database-driven REST API developed using Flask, SQLite, and Streamlit.

## Technologies
- Python
- Flask
- SQLite
- Streamlit
- Requests
- Pandas

## Features
- View all student records
- View a student by ID
- Add a new student
- Update student information
- Delete student records
- Refresh records automatically

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /students | Get all students |
| GET | /students/{id} | Get student by ID |
| POST | /students | Add student |
| PUT | /students/{id} | Update student |
| DELETE | /students/{id} | Delete student |

## How to Run

Install dependencies:

pip install -r requirements.txt

Start Flask:

python app.py

Start Streamlit in another terminal:

streamlit run frontend.py

Flask: http://127.0.0.1:5001

Streamlit: http://localhost:8501

## Demonstration Video

Add the public demonstration video link here.
