from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError
from passlib.context import CryptContext

from database import get_data_base
from config import get_settings
from domain.user import user_crud


ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().APP_JWT_EXPIRE_MINUTES
SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = get_settings().PASSWORD_ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=get_settings().APP_JWT_URL)
password_context = CryptContext(schemes=["bcrypt"])


def get_oauth2_scheme():
    return oauth2_scheme


def get_password_context():
    return password_context


def generate_user_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    data_base: Session = Depends(get_data_base),
):
    user = user_crud.get_user(data_base=data_base, user_name=form_data.username)

    if (not user) or (
        not get_password_context().verify(form_data.password, user.password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유저 이름 혹은 패스워드가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "sub": "user_token",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "user_name": user.name,
        "user_id": user.id,
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_name": user.name,
    }


def check_user_token(
    token=Depends(get_oauth2_scheme), data_base: Session = Depends(get_data_base)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("user_name")
        user_id: int = payload.get("user_id")
        if (user_name is None) or (user_id is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user_detail = user_crud.get_user_detail(
            data_base, user_name=user_name, user_id=user_id
        )
        if user_detail is None:
            raise credentials_exception

    return {"user_name": user_name, "user_id": user_id}
