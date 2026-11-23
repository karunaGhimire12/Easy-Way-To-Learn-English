from pydantic import BaseModel,EmailStr

class UserRegister(BaseModel):
    name:str
    email:EmailStr
    password:str



class Userlogin(BaseModel):
    email:EmailStr
    password:str


class RefreshTokenRequest(BaseModel):
    refresh_token:str