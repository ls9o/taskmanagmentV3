from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Option(BaseModel):
    value: str
    text: str

class Options(BaseModel):
    label: str
    show : str
    options: List[Option]

# แยก mock สำหรับสถานะลูกค้า
options_status_customer = Options(
    label='สถานะลูกค้า',
    show='/Customer',
    options=[
        Option(value="ready", text="พร้อมใช้งาน"),
        Option(value="Deactivate", text="ยกเลิกใช้งาน"),
        Option(value="lock", text="ล็อก")
    ]
)

# แยก mock สำหรับสถานะการสมัคร
options_status_registration = Options(
    label='สถานะการสมัคร',
    show='/Customer',
    options=[
        Option(value="succeed", text="สำเร็จ"),
        Option(value="cancel", text="ยกเลิก")
    ]
)

# แยก mock สำหรับสำนักงาน/สาขา
options_branch_office = Options(
    label='สำนักงาน/สาขา',
    show='/Options',
    options=[
        Option(value="paholyothin-headquarters", text="00001-สำนักพหลโยธิน (สำนักงานใหญ่)"),
        Option(value="nonthaburi", text="00002-นนทบุรี"),
        Option(value="bangbuathong", text="00003-บางบัวทอง"),
        Option(value="pathumthani", text="00004-ปทุมธานี"),

    ]
)

# แยก mock สำหรับทีมการทำงาน
options_work_team = Options(
    label='ทีมการทำงาน',
    show='/Options',
    options=[
        Option(value="admin", text="SME Admin"),
        Option(value="callcenter", text="SME Call Center"),
        Option(value="superadmin", text="SME Super Admin")
    ]
)

# แยก mock สำหรับสถานะพนักงาน
options_employee_status = Options(
    label='สถานะพนักงาน',
    show='/Options',
    options=[
        Option(value="ready", text="พร้อมใช้งาน"),
        Option(value="lock", text="ล็อก"),
        Option(value="Deactivate", text="ยกเลิกใช้งาน")
    ]
)

@router.get("/options/", response_model=List[Options])
async def get_options():
    return [
        options_status_customer,
        options_status_registration,
        options_branch_office,
        options_work_team,
        options_employee_status
    ]
