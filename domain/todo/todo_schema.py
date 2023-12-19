import datetime

from pydantic import BaseModel, field_validator


class TodoList(BaseModel):
    id: int
    user_id: int

    name: str
    create_date: datetime.datetime
    update_date: datetime.datetime | None
    is_finished: bool = False


class TotalTodoList(BaseModel):
    total: int
    todo_list: list[TodoList]


class TodoDetail(BaseModel):
    id: int
    user_id: int

    name: str
    content: str
    create_date: datetime.datetime
    update_date: datetime.datetime | None
    is_finished: bool = False


class CreateTodo(BaseModel):
    name: str
    content: str

    @field_validator("name", "content")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value


class UpdateTodo(CreateTodo):
    id: int
    is_finished: bool = False


class DeleteTodo(BaseModel):
    id: int
