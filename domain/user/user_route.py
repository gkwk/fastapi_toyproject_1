from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt

from database import get_db
from models import Todo, User
from domain.user import user_schema, user_crud
from domain.user.user_crud import passwordContext
from config import getSettings

router = APIRouter(
    prefix="/api/user",
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = getSettings().APP_JWT_SECRET_KEY
ALGORITHM = "HS256"

@router.get("/detail/{userId}", response_model=list[user_schema.UserDetail])
def getUserDetail(userId : int, db: Session = Depends(get_db)):
    userDetail = user_crud.getUserDetail(db=db,userId=userId)
    return userDetail

@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def registerUser(userCreate : user_schema.UserCreate ,db: Session = Depends(get_db)):
    if user_crud.doesUserAlreadyExist(db=db, userCreate=userCreate):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="동일한 이름 혹은 이메일을 사용중인 사용자가 이미 존재합니다.")
    user_crud.createUser(db=db,userCreate=userCreate)

@router.post("/login", response_model=user_schema.UserToken)
def loginUser(formData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.getUser(db, formData.username)
    
    if not user or not passwordContext.verify(formData.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유저 이름 혹은 패스워드가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": "userToken",
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "name" : user.name,
        "userId" : user.id,
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "accessToken": access_token,
        "tokenType": "bearer",
        "name": user.name,
        "id": user.id
    }