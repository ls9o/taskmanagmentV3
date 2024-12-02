from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()

# Define the SubInputBoxType model
class SubProcess(BaseModel):
    id: int
    idprocess : int
    subprocesdetails: str
    subprocesstart: int
    subprocesend: date

SubProcess_mock = [
    SubProcess(
        id=1,
        idprocess=1,
        subprocesdetails="Details of Process 1",
        subprocesstart=10,
        subprocesend=date(2024, 9, 10)
    ),
    SubProcess(
        id=3,
        idprocess=3,
        subprocesdetails="Details of Process 3",
        subprocesstart=20,
        subprocesend=date(2024, 9, 20)
    ),
    SubProcess(
        id=4,
        idprocess=4,
        subprocesdetails="Details of Process 4",
        subprocesstart=25,
        subprocesend=date(2024, 9, 25)
    ),
]

@router.get("/subprocess/", response_model=List[SubProcess])
async def get_subprocess():
    return SubProcess_mock

@router.post("/subprocess/")
async def create_subprocess(process: SubProcess):
    SubProcess_mock.append(process)
    return process