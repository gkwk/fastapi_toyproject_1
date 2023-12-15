from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import Todo, User
from domain.user import user_schema, user_crud

router = APIRouter(
    prefix="/api/user",
)

@router.get("/detail/{userId}", response_model=list[user_schema.UserDetail])
def getUserDetail(userId : int, db: Session = Depends(get_db)):
    userDetail = user_crud.getUserDetail(db=db,userId=userId)
    return userDetail

@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def registerUser(userCreate : user_schema.UserCreate ,db: Session = Depends(get_db)):
    if user_crud.doesUserAlreadyExist(db=db, userCreate=userCreate):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="동일한 이름 혹은 이메일을 사용중인 사용자가 이미 존재합니다.")
    user_crud.createUser(db=db,userCreate=userCreate)

@router.get("/login")
def registerUser(db: Session = Depends(get_db)):
    return "login"