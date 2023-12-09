from models import Todo
from sqlalchemy.orm import Session

def getTodoList(db: Session, userId):
    todoList = db.query(Todo).filter_by(user_id = userId).order_by(Todo.create_date.desc()).all()
    return todoList

def getTodoDetail(db: Session, userId, todoId):
    todoDetail = db.query(Todo).filter_by(user_id = userId, id = todoId)
    return todoDetail