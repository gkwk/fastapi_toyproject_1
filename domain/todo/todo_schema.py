import datetime

from pydantic import BaseModel

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