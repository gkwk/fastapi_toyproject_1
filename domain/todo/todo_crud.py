from sqlalchemy.orm import Session
from datetime import datetime

from models import Todo
from domain.todo.todo_schema import CreateTodo, UpdateTodo, DeleteTodo


def getTodoList(db: Session, userId, skip: int = 0, limit: int = 10):
    todoList = db.query(Todo).filter_by(user_id = userId).order_by(Todo.create_date.desc(),Todo.id.desc())
    total = todoList.count()
    todoList = todoList.offset(skip).limit(limit).all()
    return (total, todoList)

def getTodoDetail(db: Session, userId, todoId):
    todoDetail = db.query(Todo).filter_by(user_id = userId, id = todoId).first()
    return todoDetail

def createTodo(db: Session, schema :CreateTodo, userId : int):
    todo = Todo(user_id = userId, todo_name = schema.todo_name, text = schema.text, create_date = datetime.now())
    db.add(todo)
    db.commit()

def updateTodo(db: Session, todo: Todo, schema: UpdateTodo):
    todo.todo_name = schema.todo_name
    todo.text = schema.text
    todo.is_finished = schema.is_finished
    todo.update_date = datetime.now()
    db.add(todo)
    db.commit()
    
def deleteTodo(db: Session, todo: Todo, schema: DeleteTodo):
    db.delete(todo)
    db.commit()
