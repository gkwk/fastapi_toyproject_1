from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError

from database import GetDataBase
from models import Todo, User
from domain.todo import todo_schema, todo_crud
from domain.todo.todo_schema import CreateTodo, UpdateTodo, DeleteTodo
from config import get_settings

router = APIRouter(
    prefix="/api/todo",
)

SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


# @router.post("/list", response_model=dict[str,int|list[todo_schema.TodoList]])
@router.get("/list", response_model=todo_schema.TotalTodoList)
def getTodoList(
    token=Depends(oauth2_scheme),
    data_base: Session = Depends(GetDataBase),
    page: int = 0,
    size: int = 10,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        userId: int = payload.get("userId")
        if (name is None) or (userId is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        total, todoList = todo_crud.get_todo_list(
            data_base=data_base, userId=userId, skip=page * size, limit=size
        )
        if todoList is None:
            raise credentials_exception

    return {"total": total, "todoList": todoList}


@router.get("/detail/{todoId}", response_model=todo_schema.TodoDetail)
def getTodoDetail1(
    todoId: int, token=Depends(oauth2_scheme), db: Session = Depends(GetDataBase)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        userId: int = payload.get("userId")
        if (name is None) or (userId is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        todoDetail = todo_crud.get_todo_detail(
            data_base=db, userId=userId, todoId=todoId
        )
        if todoDetail is None:
            raise credentials_exception

    return todoDetail


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def createTodo(
    schema: CreateTodo, token=Depends(oauth2_scheme), db: Session = Depends(GetDataBase)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        userId: int = payload.get("userId")
        if (name is None) or (userId is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        if db.query(User).filter_by(id=userId).count() == 1:
            todo_crud.create_todo(data_base=db, schema=schema, userId=userId)
        else:
            raise HTTPException(status_code=404, detail="유저가 존재하지 않습니다.")


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def updateTodo(
    schema: UpdateTodo, token=Depends(oauth2_scheme), db: Session = Depends(GetDataBase)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        userId: int = payload.get("userId")
        if (name is None) or (userId is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        todoDetail = todo_crud.get_todo_detail(
            data_base=db, userId=userId, todoId=schema.todoId
        )
        if todoDetail is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
            )
        todo_crud.update_todo(data_base=db, todo=todoDetail, schema=schema)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def updateTodo(
    schema: DeleteTodo, token=Depends(oauth2_scheme), db: Session = Depends(GetDataBase)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        userId: int = payload.get("userId")
        if (name is None) or (userId is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        todoDetail = todo_crud.get_todo_detail(
            data_base=db, userId=userId, todoId=schema.todoId
        )
        if todoDetail is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
            )
        todo_crud.delete_todo(data_base=db, todo=todoDetail, schema=schema)
