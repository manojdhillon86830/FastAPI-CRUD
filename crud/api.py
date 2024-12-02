from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from .models import User
from .schema import UserCreate, UserResponse, UserUpdate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

@router.post("/send_invite")
def send_invite():
    #Here we need a email and password to send email (2 step verification turn off and less secure app is on from account settings)
    sender_email = " "  
    sender_password = " "  
    recipients = [
        "shraddha@aviato.consulting",
        "pooja@aviato.consulting",
        "prijesh@aviato.consulting",
        "hiring@aviato.consulting"
    ]
    subject = "API Documentation Link"
    api_doc_link = "http://3.106.192.149/docs#/"  

    try:
        # Set up the server
        server = smtplib.SMTP("smtp.gmail.com", 587)  
        server.starttls()
        server.login(sender_email, sender_password)

        # Create the email
        for recipient in recipients:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient
            message["Subject"] = subject

            body = f"Hello,\n\nPlease find the link to the API documentation below:\n{api_doc_link}\n\nBest Regards,\nManoj Dhillon "
            message.attach(MIMEText(body, "plain"))

            # Send the email
            server.sendmail(sender_email, recipient, message.as_string())

        server.quit()
        return {"message": "Invitation emails sent successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send emails: {str(e)}"
        )