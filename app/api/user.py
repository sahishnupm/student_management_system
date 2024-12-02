from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user import RegistrationForm, RegistrationFormResponse, LoginRequest
from app.schemas.token import Token
from app.services import user


router = APIRouter()


@router.post("/register", response_model=RegistrationFormResponse)
def register_user(
    req_model: RegistrationForm,
    db: Session = Depends(get_db)
):
    return user.register_user(db,req_model)

@router.post("/login", response_model=Token)
def login_user(req_model: LoginRequest, db: Session = Depends(get_db)):
    return user.login_user(db, req_model)




    
    