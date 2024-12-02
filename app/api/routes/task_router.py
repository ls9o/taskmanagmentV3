from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()

class Task(BaseModel):
    id: int
    infoname: str
    infodetails: str
    infostart: date
    infoend: date
    infotype: str
    manager: str
    team: str
    dayDiff: int
    progressPercentage: int
    statusprogress: int

class TaskCreate(BaseModel):
    infoname: str
    infodetails: str
    infostart: date
    infoend: date
    infotype: str
    manager: str
    team: str
    dayDiff: int
    progressPercentage: int
    statusprogress: int
    
tasks_mock = [
    Task(
        id=11,
        infoname="Task 1",
        infodetails="Details for Task 1",
        infostart=date(2024, 9, 1),
        infoend=date(2024, 9, 30),
        infotype="จัดซื้อจัดจ้าง",
        manager="Manager 1",
        team="Team A",
        dayDiff=29,
        progressPercentage=50,
        statusprogress=20,
    ),
    Task(
        id=22,
        infoname="Task 2",
        infodetails="Details for Task 1",
        infostart=date(2024, 9, 1),
        infoend=date(2024, 9, 30),
        infotype="จัดซื้อจัดจ้าง",
        manager="Manager 2",
        team="Team B",
        dayDiff=29,
        progressPercentage=50,
        statusprogress=20,
    ),
    Task(
        id=33,
        infoname="Task 3",
        infodetails="Details for Task 1",
        infostart=date(2024, 9, 1),
        infoend=date(2024, 9, 30),
        infotype="ภายใน",
        manager="Manager 1",
        team="Team A",
        dayDiff=29,
        progressPercentage=50,
        statusprogress=20,
    ),
    Task(
        id=44,
        infoname="Task 4",
        infodetails="Details for Task 1",
        infostart=date(2024, 9, 1),
        infoend=date(2024, 9, 30),
        infotype="จัดซื้อจัดจ้าง",
        manager="Manager 1",
        team="Team A",
        dayDiff=29,
        progressPercentage=50,
        statusprogress=20,
    ),
    # เพิ่มข้อมูล mock เพิ่มเติมหากจำเป็น
]

@router.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks_mock

@router.get("/tasks/{id}", response_model=Task)
def get_taskbyid(id: int):
    return tasks_mock[id - 1]

@router.post("/tasks/")
async def create_task(task: TaskCreate):
    task_id = len(tasks_mock) + 1
    new_task = Task(id=task_id, **task.model_dump())
    tasks_mock.append(new_task)
    return new_task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_data: Task):
    for index, task in enumerate(tasks_mock):
        if task.id == task_id:
            tasks_mock[index] = task_data
            tasks_mock[index].id = task_id  # ทำให้แน่ใจว่า ID ไม่เปลี่ยนแปลง
            return tasks_mock[index]
    raise HTTPException(status_code=404, detail="Task not found")

# __all__ = [tasks_mock]