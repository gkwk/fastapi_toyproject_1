from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Todo
from domain.todo import todo_schema, todo_crud

router = APIRouter(
    prefix="/api/todo",
)

@router.get("/list", response_model=list[todo_schema.Todo])
def todo_list(db: Session = Depends(get_db)):
    _todo_list = todo_crud.getTodoList(db=db)
    return _todo_list