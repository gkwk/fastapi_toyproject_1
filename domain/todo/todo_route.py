from fastapi import APIRouter

from database import SessionLocal
from models import Todo

router = APIRouter(
    prefix="/api/todo",
)

@router.get("/list")
def todo_list():
    db = SessionLocal()
    _todo_list = db.query(Todo).order_by(Todo.create_date.desc()).all()
    db.close()
    return _todo_list