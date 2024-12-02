from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Union
from .user_routerdb import User, get_db  # นำเข้า User model และ get_db จาก user_routerdb

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str
    
@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # ค้นหาผู้ใช้จากฐานข้อมูลที่มี username และ password ที่ตรงกัน
    employee_found = db.query(User).filter(User.usernamecode == user.username, User.password == user.password).first()
    
    if employee_found:
        return {
            "message": "Login successful!",
            "data": {
                "user": {
                    "userID": employee_found.usernamecode,  # ใช้ id จากฐานข้อมูลเป็น employeeID
                    "username": employee_found.firstName,
                    "LastName": employee_found.lastName,
                    "EmployeeTerm": employee_found.level,  # คุณอาจจะต้องแก้ให้ตรงกับฟิลด์ในฐานข้อมูล
                    "Branch": employee_found.Branch
                }
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
