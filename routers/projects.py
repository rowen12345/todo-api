from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import  User, Project
from schemas import ProjectCreate, ProjectOut
from database import get_db
from security import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectCreate,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    db_post = Project(name = project.name, owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
    

@router.get("/", response_model=list[ProjectOut])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Project).filter(Project.owner_id == current_user.id).all()

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    post = db.get(Project, project_id)
    if not post:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=403, detail="Forbidden — you don't own this project")
    db.delete(post)
    db.commit()
   
    return {"message": "project deleted"} 