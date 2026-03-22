from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)   
    email = Column(String, unique=True, nullable=False)  
    password = Column(String, nullable=False)
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="owner")

    
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=False)  # "high", "medium", "low"
    date = Column(String, nullable=True)        # due date
    complete = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")