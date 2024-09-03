from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, user: schemas.UserCreate):
    # Hash the password here if needed
    hashed_password = user.password
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this email or username already exists")

def get_user(db: Session, username: str,password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and user.hashed_password==password:
        return user
    return None

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()



###########
def create_log(db: Session, log: schemas.LogCreate):
    db_log = models.Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# Get logs for a specific user
def get_logs_by_user(db: Session, user_id: int):
    return db.query(models.Log).filter(models.Log.user_id == user_id).all()

def get_logs_by_date(db: Session, date: str):
    return db.query(models.Log).filter(models.Log.date == date).all()

def get_log(db: Session, log_id: int):
    return db.query(models.Log).filter(models.Log.id == log_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()