# from fastapi import APIRouter, HTTPException, Request
# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import date
# from .log_router import log_mock

# router = APIRouter()
# class User(BaseModel):
#     id: int
#     id13: int
#     RegistrationNumber: int
#     FirstName: str
#     LastName: str
#     Birthday: date
#     PhoneNumber: int
#     Mail: str
#     CustomerStatus: str
#     RegistrationDay: date
#     RegistrationStatus: str
#     DateModified: Optional[date] = None 
    
# users_mock = [
#     User(
#         id=1,
#         id13=1538389115502,
#         RegistrationNumber=123456798,
#         FirstName='John',
#         LastName='Doe',
#         Birthday=date(1985, 5, 15),
#         PhoneNumber=1234567890,
#         Mail='john.doe@example.com',
#         CustomerStatus='พร้อมใช้งาน',
#         RegistrationDay=date(2023, 1, 10),
#         RegistrationStatus='Completed',
#     ),
#     User(
#         id=2,
#         id13=7233091036758,
#         RegistrationNumber=123456798,
#         FirstName='Jane',
#         LastName='Smith',
#         Birthday=date(1987, 12, 22),
#         PhoneNumber=2345678901,
#         Mail='jane.smith@example.com',
#         CustomerStatus='ยกเลิกใช้งาน',
#         RegistrationDay=date(2023, 1, 11),
#         RegistrationStatus='Pending',
#     ),
#     User(
#         id=3,
#         id13=5828455483186,
#         RegistrationNumber=123456798,
#         FirstName='Alice',
#         LastName='Johnson',
#         Birthday=date(1990, 7, 8),
#         PhoneNumber=3456789012,
#         Mail='alice.johnson@example.com',
#         CustomerStatus='ล็อก',
#         RegistrationDay=date(2023, 1, 12),
#         RegistrationStatus='Completed',
#     ),
#     User(
#         id=4,
#         id13=3445933663572,
#         RegistrationNumber=123456798,
#         FirstName='Bob',
#         LastName='Brown',
#         Birthday=date(1992, 3, 29),
#         PhoneNumber=4567890123,
#         Mail='bob.brown@example.com',
#         CustomerStatus='ล็อก',
#         RegistrationDay=date(2023, 1, 13),
#         RegistrationStatus='Completed',
#     ),
#     User(
#         id=5,
#         id13=5911335662295,
#         RegistrationNumber=123456798,
#         FirstName='Charlie',
#         LastName='Davis',
#         Birthday=date(1989, 11, 11),
#         PhoneNumber=5678901234,
#         Mail='charlie.davis@example.com',
#         CustomerStatus='Inactive',
#         RegistrationDay=date(2023, 1, 14),
#         RegistrationStatus='Pending',
#     ),
#     User(
#         id=6,
#         id13=9970799116494,
#         RegistrationNumber=123456798,
#         FirstName='David',
#         LastName='Miller',
#         Birthday=date(1991, 9, 5),
#         PhoneNumber=6789012345,
#         Mail='david.miller@example.com',
#         CustomerStatus='Active',
#         RegistrationDay=date(2023, 1, 15),
#         RegistrationStatus='Completed',
#     ),
#     User(
#         id=7,
#         id13=6563621296258,
#         RegistrationNumber=123456798,
#         FirstName='Emma',
#         LastName='Wilson',
#         Birthday=date(1993, 6, 18),
#         PhoneNumber=7890123456,
#         Mail='emma.wilson@example.com',
#         CustomerStatus='Active',
#         RegistrationDay=date(2023, 1, 16),
#         RegistrationStatus='Completed',
#     ),
#     User(
#         id=8,
#         id13=3722028432729,
#         RegistrationNumber=123456798,
#         FirstName='Frank',
#         LastName='Moore',
#         Birthday=date(1988, 1, 10),
#         PhoneNumber=8901234567,
#         Mail='frank.moore@example.com',
#         CustomerStatus='Inactive',
#         RegistrationDay=date(2023, 1, 17),
#         RegistrationStatus='Pending',
#     ),
#     User(
#         id=9,
#         id13=7962649710144,
#         RegistrationNumber=123456798,
#         FirstName='Grace',
#         LastName='Taylor',
#         Birthday=date(1995, 8, 23),
#         PhoneNumber=9012345678,
#         Mail='grace.taylor@example.com',
#         CustomerStatus='Active',
#         RegistrationDay=date(2023, 1, 18),
#         RegistrationStatus='Completed',
#     ),
#     User(
#         id=10,
#         id13=5889787534885,
#         RegistrationNumber=123456798,
#         FirstName='Henry',
#         LastName='Anderson',
#         Birthday=date(1989, 4, 12),
#         PhoneNumber=1234567891,
#         Mail='henry.anderson@example.com',
#         CustomerStatus='Active',
#         RegistrationDay=date(2023, 1, 19),
#         RegistrationStatus='Completed',
#     )
# ]

# @router.get("/users/", response_model=List[User])
# async def get_user():
#     for user in users_mock:
#         modified_date = next((log.modified_date for log in log_mock if log.id13 == user.id13), None)
#         user.DateModified = modified_date
#     return users_mock

# @router.put("/users/{user_id}", response_model=User)
# async def update_user(user_id: int, request: Request):
#     user = next((u for u in users_mock if u.id == user_id), None)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     update_data = await request.json()

#     for key, value in update_data.items():
#         setattr(user, key, value)

#     return user



# __all__ = [users_mock]