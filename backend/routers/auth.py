from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.Token)
def register(data: schemas.SchoolRegister, db: Session = Depends(get_db)):
    existing = db.query(models.School).filter(models.School.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    school = models.School(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
    )
    db.add(school)
    db.commit()
    db.refresh(school)

    token = create_access_token({"school_id": school.id})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
def login(data: schemas.SchoolLogin, db: Session = Depends(get_db)):
    school = db.query(models.School).filter(models.School.email == data.email).first()
    if not school or not verify_password(data.password, school.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"school_id": school.id})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_me(db: Session = Depends(get_db), current_school=Depends(__import__("auth").get_current_school)):
    return {"id": current_school.id, "name": current_school.name, "email": current_school.email}
