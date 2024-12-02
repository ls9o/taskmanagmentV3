from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel,Field
from typing import List, Optional
from datetime import date

router = APIRouter()

class Employee(BaseModel):
    id: Optional[int]   # เปลี่ยน id เป็น Optional
    employeeID: str
    FirstName: str
    LastName: str
    Mail: str
    PhoneNumber: int
    Branch: str
    EmployeeStatus: str
    EmployeeTerm:str
    DateModified: Optional[date] = None  

class EmployeeCreate(BaseModel):
    employeeID: str
    FirstName: str
    LastName: str
    Mail: str
    PhoneNumber: int
    Branch: str
    EmployeeStatus: str
    EmployeeTerm:str
    DateModified: Optional[date] = None  

employee_mock = [
    Employee(
        id=1,
        employeeID="ts00001",
        FirstName='Michael',
        LastName='Johnson',
        Mail='michael.johnson@example.com',
        PhoneNumber=1987654321,
        Branch="nonthaburi",
        EmployeeStatus='ready',
        EmployeeTerm="superadmin",
    ),
    Employee(
        id=2,
        employeeID="ts00002",
        FirstName='Emily',
        LastName='Davis',
        Mail='emily.davis@example.com',
        PhoneNumber=2098765432,
        Branch="01",
        EmployeeStatus='ล็อก',
        EmployeeTerm="SME Call Center",
    ),
    Employee(
        id=3,
        employeeID="ts00003",
        FirstName='James',
        LastName='Brown',
        Mail='james.brown@example.com',
        PhoneNumber=3209876543,
        Branch="03",
        EmployeeStatus='ยกเลิกใช้งาน',
        EmployeeTerm="SME Super Admin",
    ),
    Employee(
        id=4,
        employeeID="ts00004",
        FirstName='Olivia',
        LastName='Wilson',
        Mail='olivia.wilson@example.com',
        PhoneNumber=4310987654,
        Branch="02",
        EmployeeStatus='พร้อมใช้งาน',
        EmployeeTerm="SME Admin",
    ),
    Employee(
        id=5,
        employeeID="ts00005",
        FirstName='Liam',
        LastName='Taylor',
        Mail='liam.taylor@example.com',
        PhoneNumber=5421098765,
        Branch="01",
        EmployeeStatus='ล็อก',
        EmployeeTerm="SME Admin",
    ),
    Employee(
        id=6,
        employeeID="ts00006",
        FirstName='Sophia',
        LastName='Anderson',
        Mail='sophia.anderson@example.com',
        PhoneNumber=6532109876,
        Branch="03",
        EmployeeStatus='พร้อมใช้งาน',
        EmployeeTerm="SME Admin",
    ),
    Employee(
        id=7,
        employeeID="ts00007",
        FirstName='William',
        LastName='Moore',
        Mail='william.moore@example.com',
        PhoneNumber=7643210987,
        Branch="02",
        EmployeeStatus='ยกเลิกใช้งาน',
        EmployeeTerm="SME Admin",
    ),
    Employee(
        id=8,
        employeeID="ts00008",
        FirstName='Ava',
        LastName='Jackson',
        Mail='ava.jackson@example.com',
        PhoneNumber=8754321098,
        Branch="01",
        EmployeeStatus='ล็อก',
        EmployeeTerm="SME Admin",
    ),
    Employee(
        id=9,
        employeeID="ts00009",
        FirstName='Ethan',
        LastName='White',
        Mail='ethan.white@example.com',
        PhoneNumber=9865432109,
        Branch="03",
        EmployeeStatus='พร้อมใช้งาน',
        EmployeeTerm="SME Admin",
    ),
    Employee(
        id=10,
        employeeID="ts00010",
        FirstName='Mia',
        LastName='Harris',
        Mail='mia.harris@example.com',
        PhoneNumber=1098765432,
        Branch="02",
        EmployeeStatus='พร้อมใช้งาน',
        EmployeeTerm="SME Admin",
    )
]

@router.get("/employee/", response_model=List[Employee])
async def get_employee():
    from .log_router import log_mock

    for employee in employee_mock:
        modified_date = next((log.modified_date for log in log_mock if log.employeeID == employee.employeeID), None)
        employee.DateModified = modified_date
    return employee_mock

@router.get("/employee/{id}", response_model=Employee)
def get_employeebyid(id: int):
    return employee_mock[id - 1]

@router.post("/employee/")
async def create_employee(employee: EmployeeCreate):
    employee_id = len(employee_mock) + 1
    new_employee = Employee(id=employee_id, **employee.model_dump())
    employee_mock.append(new_employee)
    return new_employee

@router.put("/employee/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, request: Request):
    existing_employee = next((u for u in employee_mock if u.id == employee_id), None)
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = await request.json()

    for key, value in update_data.items():
        setattr(existing_employee, key, value)

    return existing_employee

__all__ = [employee_mock,Employee]