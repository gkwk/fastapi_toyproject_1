from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Todo
from domain.todo import todo_schema, todo_crud

router = APIRouter(
    prefix="/api/todo",
)

@router.get("/list/{userId}", response_model=list[todo_schema.TodoList])
def getTodoList(userId : int, db: Session = Depends(get_db)):
    todoList = todo_crud.getTodoList(db=db,userId=userId)
    return todoList

@router.get("/detail/{userId}/{todoId}", response_model=list[todo_schema.TodoDetail])
def getTodoDetail(userId : int, todoId : int, db: Session = Depends(get_db)):
    todoDetail = todo_crud.getTodoDetail(db=db,userId=userId,todoId=todoId)
    return todoDetail