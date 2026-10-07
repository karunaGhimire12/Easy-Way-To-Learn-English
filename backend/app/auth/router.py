#app/auth/router.py 

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session 

from app.database import get_db 
from app.models import User 
from  app.auth.schemas import UserRegister,Userlogin
from app.auth.utils import hash_password,verify_password,create_access_token

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
def login(user:Userlogin,db:Session=Depends(get_db)):
    #find user by email 
    existing_user=db.query(User).filter(User.email==user.email).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password "
        )

    #check password 

    if not verify_password(
        user.password,
        existing_user.password_hash

    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    #login successful
    access_token=create_access_token(
        data={
            "sub":str(existing_user.id),
            "email":existing_user.email
        }
    )

    return{
        "message":"Login successful",
        "access_token":access_token,
        "token_type":"bearer"
    }

