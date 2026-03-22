from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import  User, Task
from schemas import TaskCreate, TaskOut, TaskUpdate
from database import get_db
from security import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate,current_user: User = Depends(get_current_user), db: Session = Depends(get_db) ):
    db_post = Task(name=task.name, description=task.description, 
                   priority=task.priority, date=task.date,
                   project_id=task.project_id, owner_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=list[TaskOut])
def get_tasks(project_id: int | None = None,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Task).filter(Task.owner_id == current_user.id)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    return query.all()

@router.patch("/{task_id}/complete")
def update_task_complete(task_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user) ):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_task.complete = not db_task.complete
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate,db: Session = Depends(get_db), current_user: User = Depends(get_current_user) ):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    update_data = task.model_dump(exclude_unset=True)  # only sent fields
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task



@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    post = db.get(Task, task_id)
    if not post:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=403, detail="Forbidden — you don't own this task")
    db.delete(post)
    db.commit()
   
    return {"message": "task deleted"} 