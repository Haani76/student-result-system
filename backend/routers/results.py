from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List
from database import get_db
from auth import get_current_school
import models, schemas

router = APIRouter(prefix="/results", tags=["Results"])


def calculate_grade(percentage: float) -> str:
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


@router.get("/student/{student_id}", response_model=schemas.StudentResult)
def get_result(student_id: int, db: Session = Depends(get_db), school=Depends(get_current_school)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.school_id == school.id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    marks = db.query(models.Mark).filter(models.Mark.student_id == student_id).all()
    if not marks:
        raise HTTPException(status_code=404, detail="No marks found for this student")

    subject_results = []
    total_obtained = 0
    total_marks = 0

    for mark in marks:
        subject = db.query(models.Subject).filter(models.Subject.id == mark.subject_id).first()
        pct = round(mark.obtained_marks * 100 / subject.total_marks, 2)
        subject_results.append(schemas.SubjectResult(
            subject=subject.name,
            obtained=mark.obtained_marks,
            total=subject.total_marks,
            percentage=pct,
            grade=calculate_grade(pct),
        ))
        total_obtained += mark.obtained_marks
        total_marks += subject.total_marks

    overall_pct = round(total_obtained * 100 / total_marks, 2)

    return schemas.StudentResult(
        student_name=student.name,
        roll_no=student.roll_no,
        class_name=student.class_name,
        results=subject_results,
        total_obtained=total_obtained,
        total_marks=total_marks,
        overall_percentage=overall_pct,
        overall_grade=calculate_grade(overall_pct),
    )


@router.get("/class/{class_name}/topper")
def get_class_topper(class_name: str, db: Session = Depends(get_db), school=Depends(get_current_school)):
    # Raw SQL query to find class topper
    result = db.execute(text("""
        SELECT s.name, s.roll_no, SUM(m.obtained_marks) AS total
        FROM students s
        JOIN marks m ON m.student_id = s.id
        WHERE s.school_id = :school_id AND s.class_name = :class_name
        GROUP BY s.id, s.name, s.roll_no
        ORDER BY total DESC
        LIMIT 1
    """), {"school_id": school.id, "class_name": class_name}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="No results found for this class")

    return {"name": result.name, "roll_no": result.roll_no, "total_marks": result.total}


@router.get("/class/{class_name}/report")
def get_class_report(class_name: str, db: Session = Depends(get_db), school=Depends(get_current_school)):
    # Raw SQL for class average and pass/fail count
    rows = db.execute(text("""
        SELECT s.id, s.name, s.roll_no,
               SUM(m.obtained_marks) AS obtained,
               SUM(sub.total_marks) AS total
        FROM students s
        JOIN marks m ON m.student_id = s.id
        JOIN subjects sub ON sub.id = m.subject_id
        WHERE s.school_id = :school_id AND s.class_name = :class_name
        GROUP BY s.id, s.name, s.roll_no
        ORDER BY obtained DESC
    """), {"school_id": school.id, "class_name": class_name}).fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="No data found for this class")

    report = []
    for row in rows:
        pct = round(row.obtained * 100 / row.total, 2)
        report.append({
            "name": row.name,
            "roll_no": row.roll_no,
            "total_obtained": row.obtained,
            "total_marks": row.total,
            "percentage": pct,
            "grade": calculate_grade(pct),
            "status": "Pass" if pct >= 50 else "Fail",
        })

    avg = round(sum(r["percentage"] for r in report) / len(report), 2)
    return {"class_name": class_name, "average_percentage": avg, "students": report}
