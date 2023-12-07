from models import Todo
from sqlalchemy.orm import Session

def getTodoList(db: Session):
    todoList = db.query(Todo).order_by(Todo.create_date.desc()).all()
    return todoList