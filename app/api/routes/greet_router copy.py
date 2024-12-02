from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()

# Define the SubInputBoxType model
class SubInputBoxType(BaseModel):
    id: int
    procesname: str
    procesdetails: str
    processtart: int
    procesend: date

SubInputBoxType_mock = [
    SubInputBoxType(
        id=1,
        procesname="Process 1",
        procesdetails="Details of Process 1",
        processtart=10,
        procesend=date(2024, 9, 10)
    ),
    SubInputBoxType(
        id=2,
        procesname="Process 2",
        procesdetails="Details of Process 2",
        processtart=15,
        procesend=date(2024, 9, 15)
    ),
    SubInputBoxType(
        id=3,
        procesname="Process 3",
        procesdetails="Details of Process 3",
        processtart=20,
        procesend=date(2024, 9, 20)
    ),
    SubInputBoxType(
        id=4,
        procesname="Process 4",
        procesdetails="Details of Process 4",
        processtart=25,
        procesend=date(2024, 9, 25)
    ),
    SubInputBoxType(
        id=5,
        procesname="Process 5",
        procesdetails="Details of Process 5",
        processtart=30,
        procesend=date(2024, 9, 30)
    )
]
