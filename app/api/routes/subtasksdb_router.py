from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from datetime import date
from app.database import get_db  # ฟังก์ชันสำหรับเชื่อมต่อกับฐานข้อมูล

router = APIRouter()
Base = declarative_base()

# Define the SubTask model for database
class SubTaskDB(Base):
    __tablename__ = "subtasks"  # ชื่อ table

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    idtask = Column(Integer, nullable=False)
    subinfodetails = Column(String(50), nullable=False)
    subinfostart = Column(Date, nullable=False)
    subinfoend = Column(Date, nullable=False)

# Define the SubTask model for API requests
class SubTask(BaseModel):
    idtask: int
    subinfodetails: str
    subinfostart: date
    subinfoend: date
    class Config:
        orm_mode = True

class SubTaskResponse(SubTask):
    id: int

# GET: ดึงข้อมูล subtasks ทั้งหมดจากฐานข้อมูล
@router.get("/subtasks/", response_model=List[SubTaskResponse])
def get_subtasks(db: Session = Depends(get_db)):
    subtasks = db.query(SubTaskDB).all()
    return subtasks

# POST: เพิ่มข้อมูล subtasks ใหม่
@router.post("/subtasks/", response_model=SubTaskResponse)
def create_subtask(subtask: SubTask, db: Session = Depends(get_db)):
    new_subtask = SubTaskDB(**subtask.model_dump())
    db.add(new_subtask)
    db.commit()
    db.refresh(new_subtask)
    return new_subtask

# PUT: อัปเดตข้อมูล subtask ที่มีอยู่
@router.put("/subtasks/{subtask_id}", response_model=SubTaskResponse)
def update_subtask(subtask_id: int, updated_subtask: SubTask, db: Session = Depends(get_db)):
    # ดึง subtask จากฐานข้อมูลตาม subtask_id
    db_subtask = db.query(SubTaskDB).filter(SubTaskDB.id == subtask_id).first()

    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")

    # อัปเดตข้อมูล subtask
    db_subtask.idtask = updated_subtask.idtask
    db_subtask.subinfodetails = updated_subtask.subinfodetails
    db_subtask.subinfostart = updated_subtask.subinfostart
    db_subtask.subinfoend = updated_subtask.subinfoend

    # บันทึกการเปลี่ยนแปลงลงฐานข้อมูล
    db.commit()
    db.refresh(db_subtask)

    return db_subtask

# DELETE: ลบ subtask ที่มีอยู่
@router.delete("/subtasks/{subtask_id}")
def delete_subtask(subtask_id: int, db: Session = Depends(get_db)):
    db_subtask = db.query(SubTaskDB).filter(SubTaskDB.id == subtask_id).first()

    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")

    db.delete(db_subtask)
    db.commit()
    
    return {"message": "Subtask deleted successfully"}
