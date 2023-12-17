from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt, JWTError

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
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

@router.post("/detail", response_model=user_schema.UserDetail)
def getUserDetail(token = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("name")
        id: int = payload.get("userId")
        if (name is None) or (id is None):
            raise credentialsException
    except JWTError:
        raise credentialsException
    else:
        userDetail = user_crud.getUserDetail(db, userName=name, userId=id)
        if userDetail is None:
            raise credentialsException
    
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
    accessToken = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": accessToken,
        "tokenType": "bearer",
        "name": user.name,
        "id": user.id
    }