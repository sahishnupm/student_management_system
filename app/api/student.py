from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.models import Student
from app.schemas.user import StudentRegistrationForm, StudentUpdationForm
from app.models.models import Users
from app.common.hash import get_password_hash


router = APIRouter(prefix='/student', tags=['Student'])

@router.get('')
def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.post('')
def create_student(
    req_model:StudentRegistrationForm,
    db: Session = Depends(get_db)
):  
    if db.query(Users).filter(Users.email == req_model.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(req_model.password)
    new_user = Users(name=req_model.name, email=req_model.email, password=hashed_password, role="student")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    student = Student(user_id=new_user.user_id,name=req_model.name, email=req_model.email, password=hashed_password)
    db.add(student)   
    db.commit()
    return {"message": "Student registered successfully"}


@router.put("/{student_id}")
def update_student(
    student_id: int,
    req_model: StudentUpdationForm,
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.name = req_model.name
    if req_model.password:
        student.password = get_password_hash(req_model.password)

    db.commit()
    db.refresh(student)

    return {"message": "Student updated successfully"}

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()

    return {"message": f"Student with ID {student_id} deleted successfully"}


@router.get("/{student_id}/teachers")
def get_teachers(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    teachers = student.teachers 

    return {
        "student_id": student.id,
        "student_name": student.name,
        "teachers": [{"id": teacher.id, "name": teacher.name, "email": teacher.email} for teacher in teachers],
    }