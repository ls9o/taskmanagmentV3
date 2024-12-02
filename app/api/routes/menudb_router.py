from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db 
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import List

router = APIRouter()
Base = declarative_base()

class MenuDB(Base):
    __tablename__ = "menus"
    
    id = Column(Integer, primary_key=True, index=True)
    Menuname = Column(String(100), nullable=False)
    MenuUrl = Column(String(100), nullable=False)
    Menuview = Column(String(100), nullable=False)
    icon = Column(String(100))

class Menu(BaseModel):
    Menuname: str
    MenuUrl: str
    Menuview: str
    icon: str

    class Config:
        orm_mode = True  

@router.get("/menu/", response_model=List[Menu])
async def get_menu(db: Session = Depends(get_db)):
    menus = db.query(MenuDB).all()
    return menus

@router.post("/menu/")
async def create_menu(menu: Menu, db: Session = Depends(get_db)):
    new_menu = MenuDB(**menu.model_dump())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu
