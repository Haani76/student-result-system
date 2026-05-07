from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import get_current_school
import models, schemas

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=schemas.StudentOut)
def add_student(data: schemas.StudentCreate, db: Session = Depends(get_db), school=Depends(get_current_school)):
    student = models.Student(**data.dict(), school_id=school.id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/", response_model=List[schemas.StudentOut])
def get_students(db: Session = Depends(get_db), school=Depends(get_current_school)):
    return db.query(models.Student).filter(models.Student.school_id == school.id).all()


@router.get("/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db), school=Depends(get_current_school)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.school_id == school.id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db), school=Depends(get_current_school)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.school_id == school.id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}
