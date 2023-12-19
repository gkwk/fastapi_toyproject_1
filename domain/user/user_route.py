from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError

from database import get_data_base
from models import Todo, User
from domain.user import user_schema, user_crud
from domain.user.user_crud import password_context
from config import get_settings

router = APIRouter(
    prefix="/api/user",
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = get_settings().APP_JWT_SECRET_KEY
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


@router.get("/detail", response_model=user_schema.UserDetail)
def get_user_detail(token=Depends(oauth2_scheme), db: Session = Depends(get_data_base)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        id: int = payload.get("userId")
        if (name is None) or (id is None):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        userDetail = user_crud.get_user_detail(db, userName=name, userId=id)
        if userDetail is None:
            raise credentials_exception

    return userDetail


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def register_user(
    user_create: user_schema.UserCreate, db: Session = Depends(get_data_base)
):
    if user_crud.does_user_already_exist(data_base=db, user_create=user_create):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="동일한 이름 혹은 이메일을 사용중인 사용자가 이미 존재합니다.",
        )
    user_crud.create_user(data_base=db, user_create=user_create)


@router.post("/login", response_model=user_schema.UserToken)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    data_base: Session = Depends(get_data_base),
):
    user = user_crud.get_user(data_base, form_data.username)

    if not user or not password_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유저 이름 혹은 패스워드가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": "userToken",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "name": user.name,
        "userId": user.id,
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "tokenType": "bearer",
        "name": user.name,
        "id": user.id,
    }
