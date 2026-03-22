from security import hash_password, verify_password,create_access_token
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserOut
from models import User
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate,db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:                                        # ← block if already exists
        raise HTTPException(status_code=400, detail="Email already registered")
    # happy path — no nesting needed
    hashed = hash_password(user.password)
    db_user = User(name=user.name, email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
    