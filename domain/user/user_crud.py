from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext

from models import User
from domain.user.user_schema import UserDetail, UserCreate

passwordContext = CryptContext(schemes=["bcrypt"])

def doesUserAlreadyExist(db: Session, userCreate: UserCreate):
    return db.query(User).filter((User.name == userCreate.name) | (User.email == userCreate.email)).first()

def createUser(db: Session, userCreate : UserCreate):
    user = User(name = userCreate.name, password = passwordContext.hash(userCreate.password1), join_date = datetime.now(), email = userCreate.email)
    db.add(user)
    db.commit()

def getUser(db: Session, name: str):
    user = db.query(User).filter(User.name == name).first()
    return user
    
def getUserDetail(db: Session, userId, userName):
    userDetail = db.query(User).filter_by(id = userId, name=userName).first()
    return userDetail