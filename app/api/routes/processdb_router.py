from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from datetime import date
from app.database import get_db  # ฟังก์ชันสำหรับเชื่อมต่อกับฐานข้อมูล

router = APIRouter()
Base = declarative_base()

# Define the SubInputBoxType model for database
class SubInputBoxTypeDB(Base):
    __tablename__ = "process"  # เปลี่ยนชื่อที่นี่
    
    id = Column(Integer, primary_key=True, index=True)
    idtask = Column(Integer, nullable=False)
    procesname = Column(String(50), nullable=False)
    procesdetails = Column(String(100), nullable=False)
    processtart = Column(Integer, nullable=False)
    procesend = Column(Date, nullable=False)
    processisvisible = Column(Boolean, default=False, nullable=True)

# Define the SubInputBoxType model for API requests
class SubInputBoxType(BaseModel):
    idtask: int
    procesname: str
    procesdetails: str
    processtart: int
    procesend: date
    processisvisible: bool = False
    
    class Config:
        orm_mode = True

class SubInputBoxTypeResponse(SubInputBoxType):
    id: int

@router.get("/process/", response_model=List[SubInputBoxTypeResponse])
def get_process(db: Session = Depends(get_db)):
    processes = db.query(SubInputBoxTypeDB).all()
    return processes

@router.get("/process/{idtask}", response_model=List[SubInputBoxTypeResponse])
def get_processbyidtask(idtask: int, db: Session = Depends(get_db)):
    processes = db.query(SubInputBoxTypeDB).filter(SubInputBoxTypeDB.idtask == idtask).all()
    return processes or []

@router.post("/process/", response_model=SubInputBoxTypeResponse)
def create_process(process: SubInputBoxType, db: Session = Depends(get_db)):
    new_process = SubInputBoxTypeDB(**process.model_dump())
    db.add(new_process)
    db.commit()
    db.refresh(new_process)
    return new_process

@router.put("/processes/{process_id}", response_model=SubInputBoxTypeResponse)
def update_process(process_id: int, process_data: SubInputBoxType, db: Session = Depends(get_db)):
    process = db.query(SubInputBoxTypeDB).filter(SubInputBoxTypeDB.id == process_id).first()
    
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")
    
    for key, value in process_data.model_dump().items():
        setattr(process, key, value)
    
    db.commit()
    db.refresh(process)
    return process

@router.delete("/process/{process_id}", response_model=SubInputBoxTypeResponse)
def delete_process(process_id: int, db: Session = Depends(get_db)):
    process = db.query(SubInputBoxTypeDB).filter(SubInputBoxTypeDB.id == process_id).first()
    
    if not process:
        raise HTTPException(status_code=404, detail="Process not found")

    db.delete(process)
    db.commit()
    return process