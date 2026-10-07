from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

from  app.database import get_db
from app.models import User 
from app.auth.utils import verify_access_token
from sqlalchemy.orm import Session


oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)

):
    user_id=verify_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user=db.query(User).filter(
        User.id==int(user_id)
    ).filter()



    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    return user

    
