from pydantic import BaseModel

#Auth
class UserCreate(BaseModel):
    name:str
    email:str
    password: str


class UserOut(BaseModel):
    id: int
    name:str
    email:str
    model_config = {"from_attributes": True}
    
#Projects

class ProjectCreate(BaseModel):
    name: str
    
    
class ProjectOut(BaseModel):
    id: int
    name: str
    owner_id: int
    model_config = {"from_attributes": True}
#Tasks

class TaskCreate(BaseModel):
    name: str                      # required
    description: str | None = None # optional
    priority: str                  # required
    date: str | None = None        # optional
    project_id: int                
    
class TaskOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    priority: str
    date: str | None = None
    complete: bool
    project_id: int
    owner_id: int
    model_config = {"from_attributes": True}
    
class TaskUpdate(BaseModel):
    name: str| None = None
    description: str | None = None
    priority: str| None = None
    date: str| None = None
    complete: bool| None = None
    project_id: int| None = None
    




    
