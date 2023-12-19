from datetime import datetime

from sqlalchemy.orm import Session

from models import User
from domain.user.user_schema import UserCreate
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])


def does_user_already_exist(data_base: Session, user_create: UserCreate):
    return (
        data_base.query(User)
        .filter((User.name == user_create.name) | (User.email == user_create.email))
        .first()
    )


def create_user(data_base: Session, user_create: UserCreate):
    user = User(
        name=user_create.name,
        password=password_context.hash(user_create.password1),
        join_date=datetime.now(),
        email=user_create.email,
    )
    data_base.add(user)
    data_base.commit()


def get_user(data_base: Session, user_name: str):
    user = data_base.query(User).filter(User.name == user_name).first()
    return user


def get_user_detail(data_base: Session, user_id, user_name):
    user_detail = data_base.query(User).filter_by(id=user_id, name=user_name).first()
    return user_detail
