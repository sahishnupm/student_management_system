from pydantic import BaseModel

class RegistrationForm(BaseModel):
    name : str
    email : str
    password : str
    role : str

class RegistrationFormResponse(BaseModel):
    message : str

class LoginResponse(RegistrationFormResponse):
    pass

class LoginRequest(BaseModel):
    email : str
    password : str

class StudentRegistrationForm(BaseModel):
    name : str
    email : str
    password : str

class StudentUpdationForm(BaseModel):
    name : str
    password : str