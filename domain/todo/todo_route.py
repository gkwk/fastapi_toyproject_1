from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Todo
from domain.todo import todo_schema

router = APIRouter(
    prefix="/api/todo",
)

@router.get("/list", response_model=list[todo_schema.Todo])
def todo_list(db: Session = Depends(get_db)):
    _todo_list = db.query(Todo).order_by(Todo.create_date.desc()).all()
    return _todo_list