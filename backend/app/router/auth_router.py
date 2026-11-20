#app/auth/router.py 
from datetime import datetime,timezone
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session 
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db 
from app.models import User ,RevokedToken
from  app.auth.schemas import UserRegister,Userlogin,RefreshTokenRequest
from app.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
    create_refresh_token,
    verify_refresh_token,
    decode_refresh_token
)


from app.auth.dependencies import get_current_user


router=APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user:UserRegister,db:Session=Depends(get_db)):
    print("1.Route reached")
    #Check if email already exists 
    existing_user=db.query(User).filter(User.email==user.email).first()
    print("database query worked")

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email alredy registered"
        )

    print("Email is available")

    #hash password 
    hashed_password=hash_password(user.password)
    print(hashed_password)
    #create user

    new_user=User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    print("user object created")


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "message":"User registered successfully",
        "user_id":new_user.id
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Find user using email
    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        form_data.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Generate access token
    access_token = create_access_token(
        data={
            "sub": str(existing_user.id),
            "email": existing_user.email
        }
    )

    # Generate refresh token
    refresh_token = create_refresh_token(
        data={
            "sub": str(existing_user.id),
            "email": existing_user.email
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/user_details")

def get_user_details(current_user:User=Depends(get_current_user)):
    return{
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email,
        "level":current_user.level,
        "xp":current_user.xp,
        "streak":current_user.streak
    }



@router.post("/refresh")

def refresh_access_token(request:RefreshTokenRequest,
                         db:Session=Depends(get_db)):
    user_id=verify_refresh_token(request.refresh_token)

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expire refresh token"
        )
    user=db.query(User).filter(User.id==int(user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    access_token=create_access_token(
        data={"sub":str(user.id),
              "email":user.email
              }
    )

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }



#Logout 
@router.post("/logout")
def logout(
    request:RefreshTokenRequest,
    db:Session=Depends(get_db)
):


    payload=decode_refresh_token(request.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            details="Invalid or expire refresh token"
        )


    token_jti=payload.get("jti")

    existing_token=db.query(RevokedToken).filter(
        RevokedToken.jti==token_jti
    ).first()

    if existing_token:
        return{"message":"Already logged out"}

    revoked_token=RevokedToken(
        jti=token_jti,
        expire_at=datetime.fromtimestamp(
            payload["exp"],
            tz=timezone.utc
        )
    )

    db.add(revoked_token)
    db.commit()

    return {"message":"LOgout Successful"}