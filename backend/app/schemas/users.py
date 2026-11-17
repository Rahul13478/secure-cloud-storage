from pydantic import BaseModel

class UserRegister(BaseModel):
    name : str
    user_name : str
    email : str
    password : str
    phone_number : str

class UserLogin(BaseModel):
    email : str
    password : str
    dna : str  