# app/api/routes/menu_router.py

from fastapi import APIRouter
from pydantic import BaseModel,Field
from typing import List, Optional
router = APIRouter()
# class Menu(BaseModel):
#     menu_name: str
#     menu_url: str
#     menu_view: str
#     icon:str

class Submenu(BaseModel):
    name: str
    selected_system: Optional[str] = None
    url: Optional[str] = None  # เพิ่มฟิลด์ URL สำหรับเมนูย่อย

class Menu(BaseModel):
    menu_name: str
    has_submenu: bool
    submenus: List[Submenu] = []
    selected_system: Optional[str] = None
    selected_icon: Optional[str] = None
    url: Optional[str] = None  # เพิ่มฟิลด์ URL สำหรับเมนูหลัก

# ตัวอย่างข้อมูล mock สำหรับเมนู
menu_mock = [
    {
        "menu_name": "หน้าหลัก",
        "has_submenu": False,
        "submenus": [],
        "selected_system": "HomeView",
        "selected_icon": "pi pi-users",
        "url": '/',  
    },
    # {
    #     "menu_name": "User & Team",
    #     "has_submenu": True,
    #     "submenus": [
    #         {
    #             "name": "User",
    #             "selected_system": "CustomerView",
    #             "url": "/Options"  
    #         },
    #         {
    #             "name": "Team",
    #             "selected_system": "CustomerView",
    #             "url": "/Customer"  
    #         },
            
    #     ],
    #     "selected_icon": "pi pi-box",
    #     "url": "/product",
    # },
    {
        "menu_name": "Create User & Team",
        "has_submenu": True,
        "submenus": [
            {
                "name": "Create User",
                "selected_system": "CreateUserView",
                "url": "/CreateUser"  
            },
            {
                "name": "Create Team",
                "selected_system": "CreateTeamView",
                "url": "/CreateTeam"  
            },
        ],
        "selected_icon": "pi pi-box",
        "url": "/product",
    },
    {
        "menu_name": "ติดตามงาน",
        "has_submenu": True,
        "submenus": [
            {
                "name": "New Project",
                "selected_system": "AddinfoView",
                "url": "/Addinfo" 
            },
            {
                "name": "In House",
                "selected_system": "JobInView",
                "url": "/Jobin" 
            },
            {
                "name": "Procurement",
                "selected_system": "ProcurementView",
                "url": "/Procurement" 
            },
            
        ],
        "selected_icon": "pi pi-chart-line",
        "url": "/settings", 
    },
]

# mune_mock = [
#     Menu(menu_name="ข้อมูลลูกค้า", menu_url="/Customer", menu_view="CustomerView",icon='pi pi-users'),
#     # Menu(menu_name="ตั้งค่า", menu_url="/Options", menu_view="CustomerView",icon='pi pi-cog'),
#     # Menu(menu_name="รายงาน", menu_url="/Report", menu_view="HomeView",icon='fa fa-file-text o'),
#     # Menu(menu_name="Login", menu_url="/login", menu_view="LoginView",icon='pi pi-sign-in'),
#     Menu(menu_name="Login2", menu_url="/login2", menu_view="LoginView2",icon='pi pi-sign-in'),
#     Menu(menu_name="Addinfo", menu_url="/Addinfo", menu_view="AddinfoView",icon='pi pi-inbox'),
#     Menu(menu_name="Procurement", menu_url="/Procurement", menu_view="ProcurementView",icon='pi pi-folder-open'),
#     Menu(menu_name="Jobin", menu_url="/Jobin", menu_view="JobInView",icon='pi pi-folder-open'),
#     Menu(menu_name="ผู้ใช้งาน", menu_url="/UserDetail", menu_view="UserDetails",icon='pi pi-cog'),
# ]

@router.get("/menu/", response_model=List[Menu])
async def get_menu():
    return menu_mock
