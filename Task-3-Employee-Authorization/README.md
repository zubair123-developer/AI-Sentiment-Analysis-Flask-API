
# Task 3 - Employee Authentication and Authorization

## Software Engineering Assignment 1

Employee Management REST API using Flask, SQLite,
JWT Authentication, and Role-Based Authorization.

## Technologies
- Python
- Flask
- SQLite
- PyJWT
- python-dotenv
- cURL

## User Roles

Employee:
- View employee records only

Administrator:
- View employee records
- Add employees
- Update employees
- Delete employees

## API Endpoints

| Method | Endpoint | Access |
|---|---|---|
| POST | /login | Public |
| GET | /employees | Employee and Admin |
| GET | /employees/{id} | Employee and Admin |
| POST | /employees | Admin only |
| PUT | /employees/{id} | Admin only |
| DELETE | /employees/{id} | Admin only |

## Authentication

Login generates a signed JWT token.

Protected requests use:

Authorization: Bearer YOUR_TOKEN

## HTTP Status Codes

- 200: Successful request
- 201: Employee created
- 401: Missing or invalid authentication
- 403: Insufficient permissions
- 404: Employee not found

## Setup

1. Install dependencies:

   pip install -r requirements.txt

2. Create .env from .env.example.
3. Configure the secret key and account credentials.
4. Run:

   python app.py

5. The server starts at http://127.0.0.1:5003

## Testing

Tested using cURL:
- Admin and Employee login
- Authorized employee viewing
- Administrator CRUD operations
- Employee denied administrator access
- Missing token rejected

## Demonstration Video

[Watch Task 3 Demonstration](https://drive.google.com/file/d/13mjeL3iwI667JNKN9hZZuqZx6A9s_umz/view?usp=sharing)

## Security

Real passwords, secret keys, and JWT tokens are
not stored in this repository.
