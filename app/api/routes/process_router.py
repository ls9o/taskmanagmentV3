from fastapi import APIRouter ,HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()

# Define the SubInputBoxType model
class SubInputBoxType(BaseModel):
    id: int
    idtask : int
    procesname: str
    procesdetails: str
    processtart: int
    procesend: date

SubInputBoxType_mock = [
    SubInputBoxType(
        id=1,
        idtask=1,
        procesname="Process 1",
        procesdetails="Details of Process 1",
        processtart=10,
        procesend=date(2024, 9, 10)
    ),
    SubInputBoxType(
        id=2,
        idtask=1,
        procesname="Process 2",
        procesdetails="Details of Process 2",
        processtart=15,
        procesend=date(2024, 9, 15)
    ),
    SubInputBoxType(
        id=3,
        idtask=2,
        procesname="Process 3",
        procesdetails="Details of Process 3",
        processtart=20,
        procesend=date(2024, 9, 20)
    ),
    SubInputBoxType(
        id=4,
        idtask=3,
        procesname="Process 4",
        procesdetails="Details of Process 4",
        processtart=25,
        procesend=date(2024, 9, 25)
    ),
    SubInputBoxType(
        id=6,
        idtask=1,
        procesname="Process 4",
        procesdetails="Details of Process 4",
        processtart=25,
        procesend=date(2024, 9, 25)
    ),
]

@router.get("/process/", response_model=List[SubInputBoxType])
async def get_process():
    return SubInputBoxType_mock


@router.get("/process/{id}", response_model=List[SubInputBoxType])
def get_processbyidtask(id: int):
    processes = [process for process in SubInputBoxType_mock if process.idtask == id]
    return processes or []

@router.post("/process/")
async def create_process(process: SubInputBoxType):
    SubInputBoxType_mock.append(process)
    return process

@router.put("/processes/{process_id}", response_model=SubInputBoxType)
async def update_process(process_id: int, process_data: SubInputBoxType):
    # ค้นหาข้อมูล Process ที่ตรงกับ process_id
    for index, process in enumerate(SubInputBoxType_mock):
        if process.id == process_id:
            # อัปเดตข้อมูล
            SubInputBoxType_mock[index] = process_data
            SubInputBoxType_mock[index].id = process_id  # กำหนด id ให้ตรงตาม process_id ที่อัปเดต
            return SubInputBoxType_mock[index]  # คืนค่าข้อมูลที่อัปเดต
            
    # หากไม่พบ process ที่ต้องการให้โยน HTTP Exception
    raise HTTPException(status_code=404, detail="Process not found")
