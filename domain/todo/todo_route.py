from fastapi import APIRouter

from database import SessionLocal
from models import Todo
from database import get_db

router = APIRouter(
    prefix="/api/todo",
)

@router.get("/list")
def todo_list():
    with get_db() as db:
        _todo_list = db.query(Todo).order_by(Todo.create_date.desc()).all()
    return _todo_list