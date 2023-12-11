import datetime

from pydantic import BaseModel, field_validator

class TodoList(BaseModel):
    id: int
    user_id: int
    
    todo_name : str
    create_date : datetime.datetime
    is_finished : bool = False
    
class TodoDetail(BaseModel):
    id: int
    user_id: int
    
    todo_name : str
    text : str
    create_date : datetime.datetime
    is_finished : bool = False

class CreateTodo(BaseModel):
    user_id : int
    
    todo_name : str
    text : str
    
    @field_validator("user_id")
    def isInteger(cls, value : int):
        try:
            int(value)
        except:
            raise ValueError("값이 정수여야 합니다.")
        return int(value)
    
    @field_validator("todo_name", "text")
    def isNotEmpty(cls, value : str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value