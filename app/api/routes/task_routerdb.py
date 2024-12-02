from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db  # ฟังก์ชันสำหรับเชื่อมต่อกับฐานข้อมูล
from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional
from datetime import date
from app.api.routes.user_routerdb import User
router = APIRouter()
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    infoname = Column(String(50), nullable=False)
    infodetails = Column(String(50), nullable=False)
    infostart = Column(Date, nullable=False)
    infoend = Column(Date, nullable=False)
    infotype = Column(String(50),nullable=False)
    manager = Column(String(50), nullable=False)
    userandteam = Column(JSON, nullable=False)  # ใช้ JSON สำหรับ userandteam
    dayDiff = Column(Integer, nullable=False)
    progressPercentage = Column(Integer, nullable=False)
    statusprogress = Column(Integer, nullable=False)
    create_by = Column(String(10), nullable=False)  # ฟิลด์ create_by

class TaskBase(BaseModel):
    infoname: str
    infodetails: str
    infostart: date
    infoend: date
    infotype: str
    manager: str
    userandteam: list  # ใช้ list สำหรับ JSON
    dayDiff: int
    progressPercentage: int
    statusprogress: int
    create_by: str  # ฟิลด์ create_by

class TaskUpdate(BaseModel):
    statusprogress: Optional[int]
    progressPercentage: Optional[int]

class TaskResponse(TaskBase):
    id: int

    class Config:
        orm_mode = True

class TaskBaseget(BaseModel):
    infoname: str
    infodetails: str
    infostart: date
    infoend: date
    infotype: str
    manager: str
    userandteam: str  # ใช้ list สำหรับ JSON
    dayDiff: int
    progressPercentage: int
    statusprogress: int
    create_by: str  # ฟิลด์ create_by


class TaskResponseget(TaskBaseget):
    id: int

    class Config:
        orm_mode = True

@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskBase, db: Session = Depends(get_db)):
    new_task = Task(**task.dict()) 
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/tasks/", response_model=List[TaskResponse])
def get_task(userID: str = None, id: int = None, db: Session = Depends(get_db)):
    if id is not None:
        # ดึงข้อมูล Task ตาม id
        task = db.query(Task).filter(Task.id == id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # เช็คว่าผู้ใช้มีสิทธิ์เข้าถึง task หรือไม่
        if userID:
            if task.create_by != userID:
                raise HTTPException(status_code=403, detail="You do not have permission to access this task")
        
        return [task]  # ส่งกลับเป็น list

    if userID is not None:
        # ดึงข้อมูล Task ตาม userID ของ create_by
        tasks = db.query(Task).filter(Task.create_by == userID).all()
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found for this userID")
        return tasks  # ส่งกลับ task ทั้งหมดที่ตรงกับ userID

    # ดึงข้อมูล tasks ทั้งหมด พร้อมกับ firstName และ lastName สำหรับ manager
    tasks = (
        db.query(Task, User.firstName, User.lastName)
        .outerjoin(User, User.usernamecode == Task.manager)  # ใช้ outerjoin เพื่อให้แสดงข้อมูล task แม้ไม่มี manager
        .all()
    )

    # สร้าง dictionary สำหรับ response
    task_list = []
    for task, firstName, lastName in tasks:
        # แปลง userandteam จาก JSON เป็น list ของ usernamecode
        userandteam_list = task.userandteam  # สมมติว่า userandteam เป็น list ของ usernamecode
        user_details = []  # เพื่อเก็บข้อมูลของผู้ใช้

        # ดึงข้อมูลผู้ใช้จาก userandteam
        for usernamecode in userandteam_list:
            user = db.query(User).filter(User.usernamecode == usernamecode).first()
            if user:
                user_details.append(f"{user.firstName} {user.lastName}")  # รวมชื่อและนามสกุล

        # แสดงชื่อ manager หรือค่าอื่นหากไม่มี
        manager_name = f"{firstName} {lastName}" if firstName and lastName else ''

        # สร้าง response
        task_list.append({
            "id": task.id,
            "infoname": task.infoname,
            "infodetails": task.infodetails,
            "infostart": task.infostart,
            "infoend": task.infoend,
            "infotype": task.infotype,
            "manager": manager_name,  # ชื่อของผู้จัดการหรือ 'ไม่ระบุ'
            "userandteam": user_details,  # เปลี่ยนเป็น list ของชื่อผู้ใช้
            "dayDiff": task.dayDiff,
            "progressPercentage": task.progressPercentage,
            "statusprogress": task.statusprogress,
            "create_by": task.create_by,  # เพิ่มข้อมูล create_by เพื่ออ้างอิง
        })

    return task_list

# @router.get("/tasks/", response_model=List[TaskResponse])
# def get_task(db: Session = Depends(get_db)):
#     tasks = db.query(Task).all()  # ดึงข้อมูลทั้งหมด
#     return tasks

@router.get("/tasks/{id}", response_model=TaskResponse)
def get_task_by_id(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()  # ดึงข้อมูลตาม id
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{id}", response_model=TaskResponse)
def update_task(id: int, updated_task: TaskBase, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()  # ค้นหา task ตาม id
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # อัปเดตข้อมูล task
    task.infoname = updated_task.infoname
    task.infodetails = updated_task.infodetails
    task.infostart = updated_task.infostart
    task.infoend = updated_task.infoend
    task.infotype = updated_task.infotype
    task.manager = updated_task.manager
    task.userandteam = updated_task.userandteam  # เปลี่ยนจาก team เป็น userandteam
    task.dayDiff = updated_task.dayDiff
    task.progressPercentage = updated_task.progressPercentage
    task.statusprogress = updated_task.statusprogress
    task.create_by = updated_task.create_by  # อัปเดตฟิลด์ create_by

    db.commit()  # บันทึกการเปลี่ยนแปลง
    db.refresh(task)  # รีเฟรช task
    return task

@router.patch("/tasks/{task_id}")
def partial_update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update only the fields that are provided
    if task_update.statusprogress is not None:
        task.statusprogress = task_update.statusprogress
    if task_update.progressPercentage is not None:
        task.progressPercentage = task_update.progressPercentage

    db.commit()
    db.refresh(task)
    
    return task

