from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    join_date = Column(DateTime, nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    email = Column(String, unique=True, nullable=False)

class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="Todos")
    
    todo_name = Column(Text, nullable=False)
    text = Column(String, nullable=False, default="")
    create_date = Column(DateTime, nullable=False)
    is_finished = Column(Boolean, nullable=False, default=False)