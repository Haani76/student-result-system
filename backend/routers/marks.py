from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import get_current_school
import models, schemas

router = APIRouter(prefix="/marks", tags=["Marks"])


@router.post("/", response_model=schemas.MarkOut)
def enter_marks(data: schemas.MarkCreate, db: Session = Depends(get_db), school=Depends(get_current_school)):
    # Verify student belongs to this school
    student = db.query(models.Student).filter(
        models.Student.id == data.student_id,
        models.Student.school_id == school.id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Verify subject belongs to this school
    subject = db.query(models.Subject).filter(
        models.Subject.id == data.subject_id,
        models.Subject.school_id == school.id
    ).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    if data.obtained_marks > subject.total_marks:
        raise HTTPException(status_code=400, detail=f"Marks cannot exceed total marks ({subject.total_marks})")

    # Update if already exists
    existing = db.query(models.Mark).filter(
        models.Mark.student_id == data.student_id,
        models.Mark.subject_id == data.subject_id
    ).first()

    if existing:
        existing.obtained_marks = data.obtained_marks
        db.commit()
        db.refresh(existing)
        return existing

    mark = models.Mark(**data.dict())
    db.add(mark)
    db.commit()
    db.refresh(mark)
    return mark


@router.get("/student/{student_id}", response_model=List[schemas.MarkOut])
def get_student_marks(student_id: int, db: Session = Depends(get_db), school=Depends(get_current_school)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.school_id == school.id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db.query(models.Mark).filter(models.Mark.student_id == student_id).all()
