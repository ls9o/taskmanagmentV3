from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional,Union


router = APIRouter()

class Log(BaseModel):
    id: int 
    id13: Optional[int] = None  
    employeeID: Optional[str] = None  
    modified_date: datetime  
    operatorBy:str
    changecode :str
    description: str  
    FirstName :Optional[str] =None
    EmployeeTerm :Optional[str] =None
    
log_mock = [
    Log(id= 1, id13= 9970799116494, employeeID= None, modified_date= datetime(2024, 10, 18, 5, 15, 34, 819011), operatorBy='ts00001', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 2, id13= 7962649710144, employeeID= None, modified_date= datetime(2024, 10, 9, 0, 13, 2, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 3, id13= 3722028432729, employeeID= None, modified_date= datetime(2024, 9, 20, 8, 3, 45, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 4, id13= 5911335662295, employeeID= None, modified_date= datetime(2024, 10, 16, 14, 25, 18, 819011), operatorBy='ts00003', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 5, id13= 3445933663572, employeeID= None, modified_date= datetime(2024, 10, 7, 19, 53, 36, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 6, id13= None, employeeID= 'ts00004', modified_date= datetime(2024, 10, 8, 6, 33, 19, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 7, id13= None, employeeID= 'ts00005', modified_date= datetime(2024, 9, 4, 18, 51, 18, 819011), operatorBy='ts00001', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 8, id13= None, employeeID= 'ts00008', modified_date= datetime(2024, 9, 18, 8, 36, 22, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 9, id13= None, employeeID= 'ts00003', modified_date= datetime(2024, 10, 8, 10, 2, 38, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 10, id13= 1538389115502, employeeID= None, modified_date= datetime(2024, 8, 28, 2, 30, 34, 819011), operatorBy='ts00001', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 11, id13= None, employeeID= 'ts00002', modified_date= datetime(2024, 10, 20, 19, 27, 38, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 12, id13= None, employeeID= 'ts00007', modified_date= datetime(2024, 10, 19, 17, 38, 52, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 13, id13= None, employeeID= 'ts00001', modified_date= datetime(2024, 9, 22, 5, 45, 58, 819011), operatorBy='ts00001', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 14, id13= 5889787534885, employeeID= None, modified_date= datetime(2024, 10, 15, 9, 3, 54, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 15, id13= 5828455483186, employeeID= None, modified_date= datetime(2024, 9, 27, 17, 2, 16, 819011), operatorBy='ts00001', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 16, id13= None, employeeID= 'ts00010', modified_date= datetime(2024, 10, 20, 9, 32, 29, 819011), operatorBy='ts00001', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 17, id13= 6563621296258, employeeID= None, modified_date= datetime(2024, 10, 11, 6, 17, 41, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 18, id13= None, employeeID= 'ts00006', modified_date= datetime(2024, 8, 28, 11, 41, 56, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
    Log(id= 19, id13= 7233091036758, employeeID= None, modified_date= datetime(2024, 9, 21, 18, 29, 36, 819011), operatorBy='ts00001', changecode='SME001', description= 'ข้อมูลที่มี id13'),
    Log(id= 20, id13= None, employeeID= 'ts00009', modified_date= datetime(2024, 10, 13, 7, 40, 24, 819011), operatorBy='ts00002', changecode='SME001', description= 'ข้อมูลที่มี employeeID'),
]

def get_next_changecode() -> str:
    last_changecode = max((log.changecode for log in log_mock), default="SME000")
    current_number = int(last_changecode[3:]) + 1  
    return f"SME{current_number:03d}"   

@router.get("/log/", response_model=List[Log])
async def get_log(request: Request, id: Optional[Union[int, str]] = None):
    from .employee_router import employee_mock

    if id is None:
        for log in log_mock:
            log.FirstName = next((employee.FirstName for employee in employee_mock if employee.employeeID == log.operatorBy), None)
            log.EmployeeTerm = next((employee.EmployeeTerm for employee in employee_mock if employee.employeeID == log.operatorBy), None)
        return log_mock

    filtered_logs = [log for log in log_mock if str(log.id13) == str(id) or str(log.employeeID) == str(id)]

    if filtered_logs:
        latest_log = max(filtered_logs, key=lambda log: log.modified_date)
        # เติมข้อมูล FirstName และ EmployeeTerm
        latest_log.FirstName = next((employee.FirstName for employee in employee_mock if employee.employeeID == latest_log.operatorBy), None)
        latest_log.EmployeeTerm = next((employee.EmployeeTerm for employee in employee_mock if employee.employeeID == latest_log.operatorBy), None)
        
        return [latest_log] 
    else:
        return []

@router.post("/log/")
async def create_log(request: Request):
    data = await request.json()
    log_id = len(log_mock) + 1
    changecode = get_next_changecode()
    new_log = Log(id=log_id, changecode=changecode, modified_date=datetime.now(), **data)
    log_mock.append(new_log)
    return new_log

__all__ = [log_mock]