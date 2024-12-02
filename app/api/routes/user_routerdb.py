from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from sqlalchemy import Column, Integer, String, Enum as SaEnum, Boolean
from sqlalchemy.ext.declarative import declarative_base

router = APIRouter()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(10), nullable=False)
    usernamecode = Column(String(10), unique=True, nullable=False)
    password = Column(String(10), nullable=False)
    BranchDepartment = Column(SaEnum('01', '02', '03'), default='03')
    jobposition = Column(SaEnum('01', '02', '03'), default='03')
    Branch = Column(SaEnum('01', '02'), default='02')
    level = Column(SaEnum('01', '02'), default='02')
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    neckname = Column(String(100))
    mail = Column(String(50))
    phoneNumber = Column(String(10))
    internal_contact_number = Column(String(10))
    LINEID = Column(String(100))
    is_active = Column(Boolean, default=True)

class UserCreate(BaseModel):
    username: str
    usernamecode: str
    password: str
    BranchDepartment: str = '03'
    jobposition: str = '03'
    Branch: str = '02'
    level: str = '02'
    firstName: str
    lastName: str
    neckname: str = None
    mail: str = None
    phoneNumber: str = None
    internal_contact_number: str = None
    LINEID: str = None

class UserResponse(UserCreate):
    id: int  # ต้องเพิ่มฟิลด์ id ที่จะถูกส่งออกมาใน response

    class Config:
        orm_mode = True 

@router.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.usernamecode == user.usernamecode).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usernamecode already registered")
    
    new_user_data = user.dict()
    new_user = User(**new_user_data)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}