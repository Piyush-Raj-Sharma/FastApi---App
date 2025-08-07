# # This is the first FastAPI app

from fastapi import FastAPI, Path, Query, HTTPException
# from pydantic import BaseModel, Extra 
# from typing import Optional

app = FastAPI()

# # --------------------------------------------------------------------
# # Simulated in-memory database: student records stored in a dictionary
# # --------------------------------------------------------------------
students = {
    1: {
        "name": "Aarav Mehta",
        "age": 17,
        "classs": "Grade 12",
        "email": "aarav.mehta@example.com",
        "city": "Mumbai"
    },
    2: {
        "name": "Ananya Singh",
        "age": 16,
        "classs": "Grade 11",
        "email": "ananya.singh@example.com",
        "city": "Delhi"
    },
    3: {
        "name": "Rahul Verma",
        "age": 18,
        "classs": "Grade 12",
        "email": "rahul.verma@example.com",
        "city": "Bangalore"
    },
    4: {
        "name": "Meera Nair",
        "age": 15,
        "classs": "Grade 10",
        "email": "meera.nair@example.com",
        "city": "Chennai"
    },
    5: {
        "name": "Dev Sharma",
        "age": 17,
        "classs": "Grade 11",
        "email": "dev.sharma@example.com",
        "city": "Pune"
    }
}

# # --------------------------------------------------------------------
# # Pydantic model to validate and structure student data in requests
# # --------------------------------------------------------------------
# class Student(BaseModel):
#     name: str
#     age: int
#     classs: str
#     email: str
#     city: str
    
# # --------------------------------------------------------------------
# # Pydantic model for updating student data
# # - All fields are optional to allow partial updates
# # - extra = Extra.forbid prevents unexpected fields in the request body
# #   (e.g., sending "house": 13 will raise a validation error)
# # --------------------------------------------------------------------
# class UpdateStudent(BaseModel):
#     name: Optional[str] = None
#     age: Optional[int] = None
#     classs: Optional[str] = None
#     email: Optional[str] = None
#     city: Optional[str] = None

#     class Config:  
#     # By default, Pydantic allows extra fields in the request body that are not defined in the model.
#     # Using 'extra = Extra.forbid' enforces strict validation — any unexpected or undefined fields
#     # will raise a validation error instead of being silently ignored.
#         extra = Extra.forbid

# # --------------------------------------------------------------------
# # Basic root endpoint
# # --------------------------------------------------------------------
@app.get("/")
def index():
    return {"name": "Piyush Raj Sharma"}

# # --------------------------------------------------------------------
# # Endpoint to get a student by ID
# # - Uses Path parameters with descriptions
# # - Includes additional validation using Query parameters: gt and lt
# # --------------------------------------------------------------------
@app.get("/get-student/{student_id}")
def get_student(
    student_id: int = Path(..., description="The ID of the student you want to view"), 
    gt: int = Query(..., gt=-1, description="Student ID must be greater than this value"),   
    lt: int = Query(..., lt=100, description="Student ID must be less than this value")
):
    # Check that the student_id is within allowed range
    if student_id <= gt:
        raise HTTPException(status_code=400, detail="student_id must be greater than gt")
    if student_id >= lt:
        raise HTTPException(status_code=400, detail="student_id must be less than lt")

    # If student not found in the database, return 404
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Return student data
    return students[student_id]

# # --------------------------------------------------------------------
# # Endpoint to fetch a student by query parameters
# # - Uses '*' to force keyword-only arguments (FastAPI requires this)
# # - Name is optional, age is required
# # --------------------------------------------------------------------
# @app.get("/get-by-name")
# def get_student(
#     *,
#     name: str = Query(None, description="Name of the student"),  # Optional query param
#     age: int = Query(..., description="Age of the student")       # Required query param
# ):
#     # Iterate through the student database
#     for student_id in students:
#         student = students[student_id]
#         # Match both name and age
#         if student["name"] == name and student["age"] == age:
#             return student

#     # If no match found
#     return {"data": "Student not found"}

# # --------------------------------------------------------------------
# # Endpoint to create a new student entry
# # - Accepts path param for student_id
# # - Accepts request body containing student info using Pydantic model
# # --------------------------------------------------------------------
# @app.post("/create-student/{student_id}")
# def create_student(
#     *,
#     student_id: int = Path(..., description="The ID of the student you want to create"), 
#     student: Student
# ):
#     # Prevent duplicate student entries based on student_id
#     if student_id in students:
#         return {"Error": "Student already exists"}

#     # Add new student to the in-memory database
#     students[student_id] = student
#     return students[student_id]

# # --------------------------------------------------------------------
# # This endpoint updates an existing student's information.
# # - It uses a path parameter to identify the student by ID.
# # - The request body allows partial updates using the UpdateStudent model.
# # - Each field is checked for None before updating.
# # - The update is done directly in the in-memory 'students' dictionary.
# # --------------------------------------------------------------------
# @app.put("/update-student/{student_id}")
# def update_student(
#     *,
#     student_id: int = Path(..., description="The ID of the student you want to update"),
#     student: UpdateStudent
# ):
#     # Check if the student exists
#     if student_id not in students:
#         return {"Error": "Student doesn't exist"}

#     # Update each field only if it's provided in the request
#     if student.name is not None:
#         students[student_id]['name'] = student.name
#     if student.age is not None:
#         students[student_id]['age'] = student.age
#     if student.classs is not None:
#         students[student_id]["classs"] = student.classs
#     if student.email is not None:
#         students[student_id]["email"] = student.email
#     if student.city is not None:
#         students[student_id]['city'] = student.city

#     # Return the updated student record
#     return students[student_id]

# # --------------------------------------------------------------------
# # Endpoint to delete existing student 
# # - Accepts path param for student_id
# # - Deletes the student with the specified student_id
# # --------------------------------------------------------------------
# @app.delete('/delete-student/{student_id}')
# def delete_student(student_id : int = Path(..., description="The ID of the student you want to delete")):
#     if student_id not in students:
#         return {"Error" : "Student does not exists"}
    
#     del students[student_id]
#     return {"data" : "Student deleted successfully"}
    

# # --------------------------------------------------------------------
# # Summary of Concepts Used:
# # 
# # - Path(): Used for required route/path parameters (e.g., student_id)
# # - Query(): Used for optional or validated query parameters (e.g., gt, lt)
# # - BaseModel (from Pydantic): Defines request schemas for validation and data parsing
# # - Optional[]: Allows fields to be omitted in partial updates (PATCH/PUT-style)
# # - HTTPException: Provides custom error responses with status codes
# # - '*': Forces parameters to be passed as keyword-only (helps avoid ambiguity)
# # - gt, lt, ge, le: Built-in numeric validators for query/path constraints
# # - Config(extra=Extra.forbid): Prevents request bodies from containing unexpected fields,
# #   improving strictness and avoiding silent data loss
# # - In-memory dictionary: Simulates a simple database for storing and managing student records
# # - type hints: Used for better code clarity, auto-completion, and validation
# # --------------------------------------------------------------------

