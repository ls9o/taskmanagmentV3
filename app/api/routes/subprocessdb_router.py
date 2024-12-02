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

# Define the SubProcess model for database
class SubProcessDB(Base):
    __tablename__ = "subprocess"  # เปลี่ยนชื่อที่นี่
    
    id = Column(Integer, primary_key=True, index=True)
    idprocess = Column(Integer, nullable=False)
    subprocesdetails = Column(String(100), nullable=False)
    subprocesstart = Column(Integer, nullable=False)
    subprocesend = Column(Date, nullable=False)

# Define the SubProcess model for API requests
class SubProcess(BaseModel):
    idprocess: int
    subprocesdetails: str
    subprocesstart: int
    subprocesend: date

    class Config:
        orm_mode = True

class SubProcessResponse(SubProcess):
    id: int

# GET: ดึงข้อมูล subprocess ทั้งหมดจากฐานข้อมูล
@router.get("/subprocess/", response_model=List[SubProcessResponse])
def get_subprocess(db: Session = Depends(get_db)):
    subprocesses = db.query(SubProcessDB).all()
    return subprocesses

# POST: เพิ่มข้อมูล subprocess ใหม่
@router.post("/subprocess/", response_model=SubProcessResponse)
def create_subprocess(subprocess: SubProcess, db: Session = Depends(get_db)):
    new_subprocess = SubProcessDB(**subprocess.model_dump())
    db.add(new_subprocess)
    db.commit()
    db.refresh(new_subprocess)
    return new_subprocess

# PUT: อัปเดตข้อมูล subprocess ที่มีอยู่
@router.put("/subprocess/{subprocess_id}", response_model=SubProcessResponse)
def update_subprocess(subprocess_id: int, updated_subprocess: SubProcess, db: Session = Depends(get_db)):
    # ดึง subprocess จากฐานข้อมูลตาม subprocess_id
    db_subprocess = db.query(SubProcessDB).filter(SubProcessDB.id == subprocess_id).first()

    if db_subprocess is None:
        raise HTTPException(status_code=404, detail="Subprocess not found")

    # อัปเดตข้อมูล subprocess
    db_subprocess.idprocess = updated_subprocess.idprocess
    db_subprocess.subprocesdetails = updated_subprocess.subprocesdetails
    db_subprocess.subprocesstart = updated_subprocess.subprocesstart
    db_subprocess.subprocesend = updated_subprocess.subprocesend

    # บันทึกการเปลี่ยนแปลงลงฐานข้อมูล
    db.commit()
    db.refresh(db_subprocess)

    return db_subprocess
