import datetime

from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    user_id: int
    
    todo_name : str
    text : str
    create_date : datetime.datetime
    is_finished : bool = False
    