from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from app.database import get_db
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

router = APIRouter()
Base = declarative_base()

# SQLAlchemy model สำหรับตาราง teams
class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    teamname = Column(String(10), nullable=False)
    user = Column(JSON)

# Pydantic model สำหรับการรับข้อมูลทีม
class TeamCreate(BaseModel):
    teamname: str
    user: Dict[str, str]  # เปลี่ยนจาก Json เป็น Dict

class TeamResponse(TeamCreate):
    id: int  # ต้องเพิ่มฟิลด์ id ที่จะถูกส่งออกมาใน response
    
    class Config:
        orm_mode = True

# API สำหรับดึงข้อมูลทีมทั้งหมด
@router.get("/teams/", response_model=List[TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    return teams

# API สำหรับดึงข้อมูลทีมตาม ID
@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# API สำหรับสร้างทีมใหม่
@router.post("/teams/", response_model=TeamResponse)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):  # เปลี่ยนจาก TeamResponse เป็น TeamCreate
    new_team = Team(teamname=team.teamname, user=team.user)
    
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@router.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}