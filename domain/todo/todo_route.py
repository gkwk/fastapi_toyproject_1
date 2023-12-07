from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Todo

router = APIRouter(
    prefix="/api/todo",
)

@router.get("/list")
def todo_list(db: Session = Depends(get_db)):
    _todo_list = db.query(Todo).order_by(Todo.create_date.desc()).all()
    return _todo_list