from fastapi import HTTPException
from app.models.models import Users, Student, Teacher, Log
from app.common.hash import verify_password, get_password_hash
from datetime import timedelta
from app.common.token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,verify_token
from app.schemas.token import Token

def register_user(db, req_model):
    if req_model.role not in ["student", "teacher"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    if db.query(Users).filter(Users.email == req_model.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(req_model.password)
    
    new_user = Users(name=req_model.name, email=req_model.email, password=hashed_password, role=req_model.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    if req_model.role == "student":
        student = Student(user_id=new_user.user_id,name=req_model.name, email=req_model.email, password=hashed_password)
        db.add(student)
    else:  
        teacher = Teacher(user_id=new_user.user_id,name=req_model.name, email=req_model.email, password=hashed_password)
        db.add(teacher)
    
    db.commit()
    return {"message": "User registered successfully"}


def login_user(db, req_model):
    user = db.query(Users).filter(Users.email == req_model.email).first()
    if not user: 
        raise HTTPException(status_code=401, detail="Invalid email")
    
    if not verify_password(req_model.password,user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    log = Log(user_id=user.user_id,name=user.name)
    db.add(log)
    db.commit()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
