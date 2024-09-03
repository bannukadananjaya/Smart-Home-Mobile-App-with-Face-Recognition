from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..database import SessionLocal

router = APIRouter()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a log entry
@router.post("/logs/", response_model=schemas.Log)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    db_log = crud.create_log(db=db, log=log)
    return db_log

# Get log entries for a specific user
@router.get("/logs/{user_id}", response_model=List[schemas.Log])
def read_logs(user_id: int, db: Session = Depends(get_db)):
    logs = crud.get_logs_by_user(db, user_id=user_id)
    if logs is None:
        raise HTTPException(status_code=404, detail="Logs not found")
    return logs

# Get all log entries
@router.get("/logs/", response_model=List[schemas.Log])
def read_all_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logs = crud.get_all_logs(db, skip=skip, limit=limit)
    return logs


@router.get("/logs/{date}", response_model=List[schemas.Log])
def read_logs_by_date(date: str, db: Session = Depends(get_db)):
    logs = crud.get_logs_by_date(db=db, date=date)
    if not logs:
        raise HTTPException(status_code=404, detail="Logs not found")
    return logs

