from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from .models import User
from .schema import UserCreate, UserResponse, UserUpdate

router = APIRouter()

# Create User
@router.post("/add_users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    db_user = User(username=user.username, email=user.email, project_id=user.project_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get All Users
@router.get("/get_users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Get User by ID
@router.get("/get_users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update User Details
@router.patch("/update_users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    if user.project_id:
        db_user.project_id = user.project_id
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete User
@router.delete("/delete_users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
