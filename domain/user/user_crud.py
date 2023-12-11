from sqlalchemy.orm import Session
from datetime import datetime

from models import User
from domain.user.user_schema import UserDetail

def getUserDetail(db: Session, userId):
    userDetail = db.query(User).filter_by(id = userId).all()
    return userDetail