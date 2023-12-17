from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError

from database import get_db
from models import Todo, User
from domain.todo import todo_schema, todo_crud
from domain.todo.todo_schema import CreateTodo, UpdateTodo
from config import getSettings

router = APIRouter(
    prefix="/api/todo",
)

SECRET_KEY = getSettings().APP_JWT_SECRET_KEY
ALGORITHM = "HS256"
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

# @router.post("/list", response_model=dict[str,int|list[todo_schema.TodoList]]) 
@router.get("/list", response_model=todo_schema.TotalTodoList)
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

@router.get("/detail/{todoId}", response_model=todo_schema.TodoDetail)
def getTodoDetail1(todoId : int, token = Depends(oauth2Scheme), db: Session = Depends(get_db)):
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
        todoDetail = todo_crud.getTodoDetail(db=db,userId=id,todoId=todoId)
        if todoDetail is None:
            raise credentialsException
    
    return todoDetail
    
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def createTodo(schema :CreateTodo, token = Depends(oauth2Scheme),  db: Session = Depends(get_db)):
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
        if db.query(User).filter_by(id = id).count() == 1:
            todo_crud.createTodo(db=db, schema=schema, userId=id)
        else:
            raise HTTPException(status_code=404, detail="유저가 존재하지 않습니다.")
        
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def updateTodo(schema: UpdateTodo, token = Depends(oauth2Scheme), db: Session = Depends(get_db)):
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
        todoDetail = todo_crud.getTodoDetail(db=db,userId=id,todoId=schema.todoId)
        if todoDetail is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다.")
        todo_crud.updateTodo(db=db,todo=todoDetail,schema=schema)