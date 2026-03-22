from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def register_and_login(email="test@gmail.com", password="123456"):
    client.post("/auth/register", json={"name": "testuser", "email": email, "password": password})
    response = client.post("/auth/login", data={"username": email, "password": password})
    return response.json()["access_token"]

def test_register():
    response = client.post("/auth/register", json={
        "name": "testuser",
        "email": "test@gmail.com",
        "password": "123456",
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@gmail.com"
    assert "password" not in response.json()  # password never exposed
    
def test_login():
     # register first
    client.post("/auth/register", json={
        "name": "loginuser",
        "email": "login@gmail.com",
        "password": "123456"
    })
    # then login
    response = client.post("/auth/login", data={
        "username": "login@gmail.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
def test_create_project():
    token = register_and_login(email="createproject@gmail.com")
    response = client.post(
        "/projects/",
        json={"name": "test"},
        headers={"Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    
def test_get_projects():
    token = register_and_login(email="getprojects@gmail.com")
    client.post("/projects/", json={"name": "Personal"},
        headers={"Authorization": f"Bearer {token}"})
    
    response = client.get("/projects/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0  # at least one project returned
    
def test_create_task():
    # create project first
    token = register_and_login(email="createtask@gmail.com")
    project = client.post("/projects/", 
        json={"name": "Personal"},
        headers={"Authorization": f"Bearer {token}"}
    )
    project_id = project.json()["id"]
    
    # create task
    response = client.post("/tasks/",
        json={"name": "Buy milk", "priority": "high", "project_id": project_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
def test_toggle_complete():
     # create project first
    token = register_and_login(email="testtoggletask@gmail.com")
    project = client.post("/projects/", 
        json={"name": "Personal"},
        headers={"Authorization": f"Bearer {token}"}
    )
    project_id = project.json()["id"]
    
    # create task
    task = client.post("/tasks/",
        json={"name": "Buy milk", "priority": "high", "project_id": project_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = task.json()["id"]
    
    # toggle — no body needed
    response = client.patch(f"/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["complete"] == True  # was False, now True

def test_update_task():
      # create project first
    token = register_and_login(email="testupdatetask@gmail.com")
    project = client.post("/projects/", 
        json={"name": "Personal"},
        headers={"Authorization": f"Bearer {token}"}
    )
    project_id = project.json()["id"]
    
    # create task
    task = client.post("/tasks/",
        json={"name": "Buy milk", "priority": "high", "project_id": project_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = task.json()["id"]
    response = client.patch(f"/tasks/{task_id}",
        json={"priority": "low"},  # ← add this
        headers={"Authorization": f"Bearer {token}"}
    )   
    assert response.status_code == 200
    assert response.json()["priority"] == "low"  # verify it actually updated
def test_delete_task():
      # create project first
    token = register_and_login(email="deletetask@gmail.com")
    project = client.post("/projects/", 
        json={"name": "Personal"},
        headers={"Authorization": f"Bearer {token}"}
    )
    project_id = project.json()["id"]
    
    # create task
    task = client.post("/tasks/",
        json={"name": "Buy milk", "priority": "high", "project_id": project_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = task.json()["id"]
    response = client.delete(f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # runs before each test session — clears all data
def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)