
import os
import sqlite3
import hmac
import jwt

from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

EMPLOYEE_USERNAME = os.getenv("EMPLOYEE_USERNAME")
EMPLOYEE_PASSWORD = os.getenv("EMPLOYEE_PASSWORD")

DATABASE = "employees.db"

# Define two user roles
USERS = {
    ADMIN_USERNAME: {
        "password": ADMIN_PASSWORD,
        "role": "admin"
    },
    EMPLOYEE_USERNAME: {
        "password": EMPLOYEE_PASSWORD,
        "role": "employee"
    }
}

# Check configuration before starting
if not all([
    SECRET_KEY,
    ADMIN_USERNAME,
    ADMIN_PASSWORD,
    EMPLOYEE_USERNAME,
    EMPLOYEE_PASSWORD
]):
    raise RuntimeError("Please configure all values in .env")

if ADMIN_USERNAME == EMPLOYEE_USERNAME:
    raise RuntimeError("Admin and Employee usernames must be different")


# Connect to SQLite database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create employees table
def create_table():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)


# Login endpoint - Generate JWT
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    username = data.get("username", "")
    password = data.get("password", "")

    user = USERS.get(username) if isinstance(username, str) else None

    if (
        not user
        or not isinstance(password, str)
        or not hmac.compare_digest(password, user["password"])
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "username": username,
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "role": user["role"],
        "token": token
    }), 200


# Authentication and authorization decorator
def token_required(admin_only=False):
    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization", "")

            if not auth.startswith("Bearer "):
                return jsonify({
                    "error": "Missing Bearer token"
                }), 401

            token = auth[7:]

            try:
                payload = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=["HS256"]
                )
            except jwt.InvalidTokenError:
                return jsonify({
                    "error": "Invalid or expired token"
                }), 401

            username = payload.get("username")
            role = payload.get("role")

            user = USERS.get(username)

            if not user or user["role"] != role:
                return jsonify({
                    "error": "Invalid user or role"
                }), 401

            if admin_only and role != "admin":
                return jsonify({
                    "error": "Administrator access required"
                }), 403

            return function(*args, **kwargs)

        return wrapper

    return decorator


# GET - View all employees
@app.route("/employees", methods=["GET"])
@token_required()
def get_employees():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM employees ORDER BY id"
        ).fetchall()

    return jsonify([dict(row) for row in rows]), 200


# GET - View employee by ID
@app.route("/employees/<int:id>", methods=["GET"])
@token_required()
def get_employee(id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM employees WHERE id = ?",
            (id,)
        ).fetchone()

    if row is None:
        return jsonify({
            "error": "Employee not found"
        }), 404

    return jsonify(dict(row)), 200


# POST - Add employee (Admin only)
@app.route("/employees", methods=["POST"])
@token_required(admin_only=True)
def add_employee():
    data = request.get_json(silent=True) or {}

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    name = str(data.get("name") or "").strip()
    department = str(data.get("department") or "").strip()
    email = str(data.get("email") or "").strip()

    if not all([name, department, email]):
        return jsonify({
            "error": "All fields are required"
        }), 400

    try:
        with get_db() as conn:
            cursor = conn.execute(
                """
                INSERT INTO employees (name, department, email)
                VALUES (?, ?, ?)
                """,
                (name, department, email)
            )

            employee_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Email already exists"
        }), 409

    return jsonify({
        "message": "Employee added successfully",
        "id": employee_id
    }), 201


# PUT - Update employee (Admin only)
@app.route("/employees/<int:id>", methods=["PUT"])
@token_required(admin_only=True)
def update_employee(id):
    data = request.get_json(silent=True) or {}

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    with get_db() as conn:
        employee = conn.execute(
            "SELECT * FROM employees WHERE id = ?",
            (id,)
        ).fetchone()

        if employee is None:
            return jsonify({
                "error": "Employee not found"
            }), 404

        name = str(data.get("name", employee["name"]) or "").strip()
        department = str(
            data.get("department", employee["department"]) or ""
        ).strip()
        email = str(data.get("email", employee["email"]) or "").strip()

        if not all([name, department, email]):
            return jsonify({
                "error": "Fields cannot be empty"
            }), 400

        try:
            conn.execute(
                """
                UPDATE employees
                SET name = ?, department = ?, email = ?
                WHERE id = ?
                """,
                (name, department, email, id)
            )

        except sqlite3.IntegrityError:
            return jsonify({
                "error": "Email already exists"
            }), 409

    return jsonify({
        "message": "Employee updated successfully"
    }), 200


# DELETE - Remove employee (Admin only)
@app.route("/employees/<int:id>", methods=["DELETE"])
@token_required(admin_only=True)
def delete_employee(id):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM employees WHERE id = ?",
            (id,)
        )

        if cursor.rowcount == 0:
            return jsonify({
                "error": "Employee not found"
            }), 404

    return jsonify({
        "message": "Employee deleted successfully"
    }), 200


# Start Flask server
if __name__ == "__main__":
    create_table()

    app.run(
        host="127.0.0.1",
        port=5003,
        debug=False,
        use_reloader=False
    )
