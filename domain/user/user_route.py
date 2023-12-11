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