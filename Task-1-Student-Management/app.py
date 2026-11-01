
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "students.db"


# Connect to SQLite database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create students table
def create_table():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)


# GET - Retrieve all students
@app.route("/students", methods=["GET"])
def get_students():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

    return jsonify([dict(row) for row in rows])


# GET - Retrieve one student by ID
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?", (id,)
        ).fetchone()

    if row is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(row))


# POST - Add a new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name") or "").strip()
    department = str(data.get("department") or "").strip()
    email = str(data.get("email") or "").strip()

    if not name or not department or not email:
        return jsonify({"error": "All fields are required"}), 400

    try:
        with get_db() as conn:
            cursor = conn.execute(
                "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
                (name, department, email)
            )
            student_id = cursor.lastrowid

        return jsonify({
            "message": "Student added successfully",
            "id": student_id
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409


# PUT - Update an existing student
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.get_json(silent=True) or {}

    with get_db() as conn:
        existing = conn.execute(
            "SELECT * FROM students WHERE id = ?", (id,)
        ).fetchone()

        if existing is None:
            return jsonify({"error": "Student not found"}), 404

        name = str(data.get("name", existing["name"]) or "").strip()
        department = str(
            data.get("department", existing["department"]) or ""
        ).strip()
        email = str(data.get("email", existing["email"]) or "").strip()

        if not name or not department or not email:
            return jsonify({"error": "Fields cannot be empty"}), 400

        try:
            conn.execute(
                """
                UPDATE students
                SET name = ?, department = ?, email = ?
                WHERE id = ?
                """,
                (name, department, email, id)
            )
        except sqlite3.IntegrityError:
            return jsonify({"error": "Email already exists"}), 409

    return jsonify({"message": "Student updated successfully"})


# DELETE - Remove a student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?", (id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})


if __name__ == "__main__":
    create_table()
    app.run(port=5001, debug=False, use_reloader=False)
