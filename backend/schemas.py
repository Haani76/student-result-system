from pydantic import BaseModel, EmailStr
from typing import Optional, List


# --- Auth ---
class SchoolRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class SchoolLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# --- Student ---
class StudentCreate(BaseModel):
    name: str
    roll_no: str
    class_name: str


class StudentOut(BaseModel):
    id: int
    name: str
    roll_no: str
    class_name: str

    class Config:
        from_attributes = True


# --- Subject ---
class SubjectCreate(BaseModel):
    name: str
    total_marks: int = 100


class SubjectOut(BaseModel):
    id: int
    name: str
    total_marks: int

    class Config:
        from_attributes = True


# --- Marks ---
class MarkCreate(BaseModel):
    student_id: int
    subject_id: int
    obtained_marks: int


class MarkOut(BaseModel):
    id: int
    student_id: int
    subject_id: int
    obtained_marks: int

    class Config:
        from_attributes = True


# --- Result ---
class SubjectResult(BaseModel):
    subject: str
    obtained: int
    total: int
    percentage: float
    grade: str


class StudentResult(BaseModel):
    student_name: str
    roll_no: str
    class_name: str
    results: List[SubjectResult]
    total_obtained: int
    total_marks: int
    overall_percentage: float
    overall_grade: str
