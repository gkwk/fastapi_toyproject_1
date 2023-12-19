from sqlalchemy.orm import Session
from datetime import datetime

from models import Todo
from domain.todo.todo_schema import CreateTodo, UpdateTodo, DeleteTodo


def get_todo_list(data_base: Session, userId, skip: int = 0, limit: int = 10):
    todo_list = (
        data_base.query(Todo)
        .filter_by(user_id=userId)
        .order_by(Todo.create_date.desc(), Todo.id.desc())
    )
    total = todo_list.count()
    todo_list = todo_list.offset(skip).limit(limit).all()
    return (total, todo_list)


def get_todo_detail(data_base: Session, userId, todoId):
    todo_detail = data_base.query(Todo).filter_by(user_id=userId, id=todoId).first()
    return todo_detail


def create_todo(data_base: Session, schema: CreateTodo, userId: int):
    todo = Todo(
        user_id=userId,
        todo_name=schema.todo_name,
        text=schema.text,
        create_date=datetime.now(),
    )
    data_base.add(todo)
    data_base.commit()


def update_todo(data_base: Session, todo: Todo, schema: UpdateTodo):
    todo.todo_name = schema.todo_name
    todo.text = schema.text
    todo.is_finished = schema.is_finished
    todo.update_date = datetime.now()
    data_base.add(todo)
    data_base.commit()


def delete_todo(data_base: Session, todo: Todo, schema: DeleteTodo):
    data_base.delete(todo)
    data_base.commit()
