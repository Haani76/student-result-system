from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import get_current_school
import models, schemas

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.post("/", response_model=schemas.SubjectOut)
def add_subject(data: schemas.SubjectCreate, db: Session = Depends(get_db), school=Depends(get_current_school)):
    subject = models.Subject(**data.dict(), school_id=school.id)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("/", response_model=List[schemas.SubjectOut])
def get_subjects(db: Session = Depends(get_db), school=Depends(get_current_school)):
    return db.query(models.Subject).filter(models.Subject.school_id == school.id).all()


@router.delete("/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db), school=Depends(get_current_school)):
    subject = db.query(models.Subject).filter(
        models.Subject.id == subject_id,
        models.Subject.school_id == school.id
    ).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted"}
