
from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI(title="Student Management API")

# JSON file location
FILE = Path(__file__).parent / "students.json"


# Read students from JSON file
def read_students():
    with open(FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Save students to JSON file
def save_students(students):
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


# GET: Retrieve all students
@app.get("/students")
def get_students(dept: str = None):
    students = read_students()

    if dept is not None:
        result = []

        for student in students:
            if student["dept"] == dept:
                result.append(student)

        return result

    return students


# GET: Retrieve one student by ID
@app.get("/students/{student_id}")
def get_student_id(student_id: int):
    students = read_students()

    for student in students:
        if student["id"] == student_id:
            return student

    return {"message": "Student ID is invalid"}


# POST: Add a new student
@app.post("/students")
def add_student(student: dict):
    students = read_students()

    student["id"] = max(
        [s["id"] for s in students],
        default=0
    ) + 1

    students.append(student)
    save_students(students)

    return {
        "message": "Student added successfully",
        "students": students
    }


# PUT: Update a student's details
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: dict):
    students = read_students()

    for student in students:
        if student["id"] == student_id:
            student["name"] = updated_student["name"]
            student["dept"] = updated_student["dept"]

            save_students(students)

            return {
                "message": "Student updated successfully",
                "student": student
            }

    return {"message": "Student ID is invalid"}


# DELETE: Remove a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    students = read_students()

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_students(students)

            return {
                "message": "Student deleted successfully",
                "students": students
            }

    return {"message": "Student ID is invalid"}

