# from sqlalchemy import Column, Integer, String, Date
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Task(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True, index=True)
#     infoname = Column(String(255), nullable=False)
#     infodetails = Column(String(255))
#     infostart = Column(Date)
#     infoend = Column(Date)
#     infotype = Column(String(50))
#     manager = Column(String(100))
#     team = Column(String(255))
#     dayDiff = Column(Integer)
#     progressPercentage = Column(Integer)
#     statusprogress = Column(Integer)
