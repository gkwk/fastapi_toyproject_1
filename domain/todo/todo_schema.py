import datetime

from pydantic import BaseModel, field_validator

class TodoList(BaseModel):
    id: int
    user_id: int
    
    todo_name : str
    create_date : datetime.datetime
    update_date : datetime.datetime | None
    is_finished : bool = False
    
class TotalTodoList(BaseModel):
    total : int
    todoList : list[TodoList]
    
class TodoDetail(BaseModel):
    id: int
    user_id: int
    
    todo_name : str
    text : str
    create_date : datetime.datetime
    update_date : datetime.datetime | None
    is_finished : bool = False

class CreateTodo(BaseModel):
    todo_name : str
    text : str
    
    @field_validator("todo_name", "text")
    def isNotEmpty(cls, value : str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value
    
class UpdateTodo(CreateTodo):
    todoId : int