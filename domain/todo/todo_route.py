from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError

from database import get_db
from models import Todo, User
from domain.todo import todo_schema, todo_crud
from domain.todo.todo_schema import CreateTodo
from config import getSettings

router = APIRouter(
    prefix="/api/todo",
)

SECRET_KEY = getSettings().APP_JWT_SECRET_KEY
ALGORITHM = "HS256"
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

# @router.post("/list", response_model=dict[str,int|list[todo_schema.TodoList]]) 
@router.post("/list", response_model=todo_schema.TotalTodoList)
def getTodoList(token = Depends(oauth2Scheme), db: Session = Depends(get_db), page: int = 0, size: int = 10):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        id: int = payload.get("userId")
        if (name is None) or (id is None):
            raise credentialsException
    except JWTError:
        raise credentialsException
    else:
        total, todoList = todo_crud.getTodoList(db=db,userId=id,skip=page*size, limit=size)
        if todoList is None:
            raise credentialsException
    
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