import datetime

from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

from domain.todo.todo_schema import TodoDetail


class UserCreate(BaseModel):
    name: str
    password1: str
    password2: str
    email: EmailStr

    @field_validator("name", "password1", "password2", "email")
    def is_not_empty(cls, value: str):
        if not value.strip():
            raise ValueError("값이 공백일 수 없습니다.")
        return value

    @field_validator("password2")
    def password_confirm(cls, value, info: FieldValidationInfo):
        # print(info) ValidationInfo(config={'title': 'UserCreate'}, context=None, data={'name': 'string', 'password1': 'string'}, field_name='password2')
        if "password1" in info.data and value != info.data["password1"]:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return value


class UserToken(BaseModel):
    # 규칙에 따라 access_token은 access_token으로 두어야 한다.
    access_token: str
    token_type: str
    user_name: str
    user_id: int


class UserDetail(BaseModel):
    id: int

    name: str
    password: str
    join_date: datetime.datetime
    is_superuser: bool = False

    Todos: list[TodoDetail] = []
