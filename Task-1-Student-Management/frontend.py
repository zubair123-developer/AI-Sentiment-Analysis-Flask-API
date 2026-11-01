
import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5001"

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Management System")
st.write("Software Engineering Assignment 1 - Task 1")
st.write("Flask REST API + SQLite + Streamlit")

# Function to request student records from Flask
def load_students():
    response = requests.get(
        f"{API_URL}/students", timeout=10
    )
    response.raise_for_status()
    return response.json()


# Display all students
st.subheader("Student Records")

try:
    students = load_students()
    if students:
        df = pd.DataFrame(students)
        st.dataframe(df, use_container_width=True,
                     hide_index=True)
    else:
        st.info("No student records available.")
except requests.RequestException:
    st.error("Cannot connect to Flask API on port 5001.")
    st.stop()


# Add student
st.subheader("Add New Student")

with st.form("add_student_form"):
    name = st.text_input("Student Name")
    department = st.text_input("Department")
    email = st.text_input("Email Address")
    add_button = st.form_submit_button("Add Student")

    if add_button:
        if not name.strip() or not department.strip() or not email.strip():
            st.warning("Please fill all fields.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/students",
                    json={
                        "name": name.strip(),
                        "department": department.strip(),
                        "email": email.strip()
                    },
                    timeout=10
                )
                if response.status_code == 201:
                    st.success("Student added successfully!")
                    st.rerun()
                else:
                    st.error(response.json().get("error", "Failed to add student"))
            except requests.RequestException as error:
                st.error(f"API error: {error}")


# Update student
st.subheader("Update Student")

if students:
    student_options = {
        f"{s['id']} - {s['name']}": s
        for s in students
    }

    selected_label = st.selectbox(
        "Select Student to Update",
        list(student_options.keys())
    )

    selected_student = student_options[selected_label]

    with st.form(f"update_form_{selected_student['id']}"):
        new_name = st.text_input(
            "New Name", value=selected_student["name"]
        )
        new_department = st.text_input(
            "New Department",
            value=selected_student["department"]
        )
        new_email = st.text_input(
            "New Email", value=selected_student["email"]
        )

        update_button = st.form_submit_button("Update Student")

        if update_button:
            try:
                response = requests.put(
                    f"{API_URL}/students/{selected_student['id']}",
                    json={
                        "name": new_name,
                        "department": new_department,
                        "email": new_email
                    },
                    timeout=10
                )
                if response.ok:
                    st.success("Student updated successfully!")
                    st.rerun()
                else:
                    st.error(response.json().get("error", "Update failed"))
            except requests.RequestException as error:
                st.error(f"API error: {error}")
else:
    st.info("Add a student before updating records.")


# Delete student
st.subheader("Delete Student")

if students:
    delete_options = {
        f"{s['id']} - {s['name']}": s["id"]
        for s in students
    }

    delete_label = st.selectbox(
        "Select Student to Delete",
        list(delete_options.keys())
    )

    confirm_delete = st.checkbox(
        "I confirm I want to delete this student"
    )

    if st.button("Delete Student"):
        if not confirm_delete:
            st.warning("Please confirm deletion first.")
        else:
            try:
                student_id = delete_options[delete_label]
                response = requests.delete(
                    f"{API_URL}/students/{student_id}",
                    timeout=10
                )
                if response.ok:
                    st.success("Student deleted successfully!")
                    st.rerun()
                else:
                    st.error(response.json().get("error", "Delete failed"))
            except requests.RequestException as error:
                st.error(f"API error: {error}")
else:
    st.info("No students available to delete.")


# Refresh records
if st.button("Refresh Student Records"):
    st.rerun()
