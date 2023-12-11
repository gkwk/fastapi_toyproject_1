import datetime

from pydantic import BaseModel, field_validator
from domain.todo.todo_schema import TodoDetail


class UserDetail(BaseModel):
    id: int
        
    name : str
    password : str
    join_date : datetime.datetime
    is_superuser : bool = False
    
    Todos : list[TodoDetail] = []