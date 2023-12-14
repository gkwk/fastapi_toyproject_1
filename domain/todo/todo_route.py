from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import Todo, User
from domain.todo import todo_schema, todo_crud
from domain.todo.todo_schema import CreateTodo

router = APIRouter(
    prefix="/api/todo",
)

# @router.get("/list/{userId}", response_model=dict[str,int|list[todo_schema.TodoList]]) 
@router.get("/list/{userId}", response_model=todo_schema.TotalTodoList)
def getTodoList(userId : int, db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, todoList = todo_crud.getTodoList(db=db,userId=userId,skip=page*size, limit=size)
    return {"total" : total, "todoList" : todoList}

@router.get("/detail/{userId}/{todoId}", response_model=list[todo_schema.TodoDetail])
def getTodoDetail(userId : int, todoId : int, db: Session = Depends(get_db)):
    todoDetail = todo_crud.getTodoDetail(db=db,userId=userId,todoId=todoId)
    return todoDetail

@router.post("/create/{userId}", status_code=status.HTTP_204_NO_CONTENT)
def createTodo(schema :CreateTodo ,db: Session = Depends(get_db)):
    if  db.query(User).filter_by(id = schema.user_id).count() == 1:
        # userid 검증 방법 개선 필요
        todo_crud.createTodo(db=db, schema=schema)
    else:
        raise HTTPException(status_code=404, detail="User not found")