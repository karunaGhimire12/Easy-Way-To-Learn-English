#backend/app/auth/security.py

import os 
import uuid
from datetime  import datetime,timedelta

from passlib.context import CryptContext
from jose import jwt,JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30")
)

REFRESH_TOKEN_EXPIRE_DAYS=int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS","7")
)

pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"

)


def hash_password(password:str)->str:
    return pwd_context.hash(password)


def verify_password(
        plain_password:str,
        hashed_password:str
)->bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+ timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp":expire,
         "type":"access"}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


#verify access_token 

def verify_access_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )

        if payload.get("type") != "access":
            return None

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return user_id

     

    except JWTError:
        return None 



def create_refresh_token(data:dict):
    to_encode=data.copy()
    #generate a unique ID for this token
    jti=str(uuid.uuid4())

    expire=datetime.utcnow()+timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )


    to_encode.update({
        "exp":expire,
        "type":"refresh",
        "jti":jti
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )



def verify_refresh_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        if (payload.get("type")!="refresh"):
            return None

        user_id=payload.get("sub")

        if user_id is None:
            return None
        return user_id

    except JWTError:
        return None
    

def decode_refresh_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        #check whether this is a refresh token
        if payload.get("type")!="refresh":
            return None

        if not payload.get("sub"):
            return None

        if not payload.get("jti"):
            return None

        if not payload.get("exp"):
            return None
    except JWTError:
        return None 

    return payload

