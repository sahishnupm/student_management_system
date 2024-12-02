from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime


student_teacher = Table(
    'student_teacher',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('student_management.id'), primary_key=True),
    Column('teacher_id', Integer, ForeignKey('teacher_management.id'), primary_key=True)
)

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum("student", "teacher", name="user_roles"), nullable=False)

class Student(Base):
    __tablename__ = 'student_management'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    teachers = relationship("Teacher", secondary=student_teacher, back_populates="students")

class Teacher(Base):
    __tablename__ = 'teacher_management'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    students = relationship("Student", secondary=student_teacher, back_populates="teachers")

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, nullable=False)
    signed_in_time = Column(DateTime, default=datetime.utcnow)



