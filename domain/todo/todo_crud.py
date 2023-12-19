from sqlalchemy.orm import Session
from datetime import datetime

from models import Todo
from domain.todo.todo_schema import CreateTodo, UpdateTodo, DeleteTodo


def get_todo_list(data_base: Session, user_id: int, skip: int = 0, limit: int = 10):
    todo_list = (
        data_base.query(Todo)
        .filter_by(user_id=user_id)
        .order_by(Todo.create_date.desc(), Todo.id.desc())
    )
    total = todo_list.count()
    todo_list = todo_list.offset(skip).limit(limit).all()
    return (total, todo_list)


def get_todo_detail(data_base: Session, user_id: int, todo_id: int):
    todo_detail = data_base.query(Todo).filter_by(user_id=user_id, id=todo_id).first()
    return todo_detail


def create_todo(data_base: Session, schema: CreateTodo, user_id: int):
    todo = Todo(
        user_id=user_id,
        name=schema.name,
        content=schema.content,
        create_date=datetime.now(),
    )
    data_base.add(todo)
    data_base.commit()


def update_todo(data_base: Session, todo: Todo, schema: UpdateTodo):
    todo.name = schema.name
    todo.content = schema.content
    todo.is_finished = schema.is_finished
    todo.update_date = datetime.now()
    data_base.add(todo)
    data_base.commit()


def delete_todo(data_base: Session, todo: Todo, schema: DeleteTodo):
    data_base.delete(todo)
    data_base.commit()
