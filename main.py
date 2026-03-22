
from fastapi import FastAPI
from database import engine, Base
from routers import projects, tasks, auth
from fastapi.middleware.cors import CORSMiddleware


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://rowen12345.github.io",
    "https://web-production-e22f.up.railway.app"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
app.include_router(auth.router)    
app.include_router(projects.router)
app.include_router(tasks.router)
    
@app.get("/")
def home():
    return {"message": "welcome to my API"}

@app.get("/about")
def about():
    return {"app": "To-do API", "version": "1.0"}




