from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_data_base
from domain.todo import todo_schema, todo_crud
from domain.todo.todo_schema import CreateTodo, UpdateTodo, DeleteTodo
from component.auth import check_user_token, get_oauth2_scheme

router = APIRouter(
    prefix="/api/todo",
)


@router.get("/list", response_model=todo_schema.TotalTodoList)
def get_todo_list(
    token=Depends(get_oauth2_scheme()),
    data_base: Session = Depends(get_data_base),
    page: int = 0,
    size: int = 10,
):
    data = check_user_token(token=token, data_base=data_base)
    total, todoList = todo_crud.get_todo_list(
        data_base=data_base, user_id=data["user_id"], skip=page * size, limit=size
    )

    if not (todoList is None):
        return {"total": total, "todo_list": todoList}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
        )


@router.get("/detail/{todo_id}", response_model=todo_schema.TodoDetail)
def get_todo_detail(
    todo_id: int,
    token=Depends(get_oauth2_scheme()),
    data_base: Session = Depends(get_data_base),
):
    data = check_user_token(token=token, data_base=data_base)
    todoDetail = todo_crud.get_todo_detail(
        data_base=data_base, user_id=data["user_id"], todo_id=todo_id
    )

    if not (todoDetail is None):
        return todoDetail
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
        )


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def create_todo(
    schema: CreateTodo,
    token=Depends(get_oauth2_scheme()),
    data_base: Session = Depends(get_data_base),
):
    data = check_user_token(token=token, data_base=data_base)
    todo_crud.create_todo(data_base=data_base, schema=schema, user_id=data["user_id"])


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(
    schema: UpdateTodo,
    token=Depends(get_oauth2_scheme()),
    data_base: Session = Depends(get_data_base),
):
    data = check_user_token(token=token, data_base=data_base)
    todoDetail = todo_crud.get_todo_detail(
        data_base=data_base, user_id=data["user_id"], todo_id=schema.id
    )

    if not (todoDetail is None):
        todo_crud.update_todo(data_base=data_base, todo=todoDetail, schema=schema)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
        )


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(
    schema: DeleteTodo,
    token=Depends(get_oauth2_scheme()),
    data_base: Session = Depends(get_data_base),
):
    data = check_user_token(token=token, data_base=data_base)
    todoDetail = todo_crud.get_todo_detail(
        data_base=data_base, user_id=data["user_id"], todo_id=schema.id
    )

    if not (todoDetail is None):
        todo_crud.delete_todo(data_base=data_base, todo=todoDetail, schema=schema)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."
        )
