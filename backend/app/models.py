from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.sql import func
from database import Base 

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True )
    name=Column(String,nullable=False)
    email=Column(String,unique=True,index=True,nullable=False)

    password_hash=Column(String,nullable=True)

    auth_provider=Column(String,default="local")
    google_id=Column(String,unique=True,nullable=True)

    level=Column(String,default="Beginner")
    xp=Column(Integer,default=0)
    streak=Column(Integer,default=0)


    created_at=Column(DateTime(timezone=True),server_default=func.now())

