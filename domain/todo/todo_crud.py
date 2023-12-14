from sqlalchemy.orm import Session
from datetime import datetime

from models import Todo
from domain.todo.todo_schema import CreateTodo


def getTodoList(db: Session, userId, skip: int = 0, limit: int = 10):
    todoList = db.query(Todo).filter_by(user_id = userId).order_by(Todo.create_date.desc(),Todo.id.desc())
    total = todoList.count()
    todoList = todoList.offset(skip).limit(limit).all()
    return (total, todoList)

def getTodoDetail(db: Session, userId, todoId):
    todoDetail = db.query(Todo).filter_by(user_id = userId, id = todoId).all()
    return todoDetail

def createTodo(db: Session, schema :CreateTodo):
    todo = Todo(user_id = schema.user_id, todo_name = schema.todo_name, text = schema.text, create_date = datetime.now())
    db.add(todo)
    db.commit()
