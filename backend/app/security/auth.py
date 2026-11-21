from passlib.context import CryptContext #used in password hashing 
from app.core.settings import setting
from jose import jwt , JWTError
from datetime import datetime , timedelta , timezone
from fastapi import Depends , HTTPException  ,status
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os 
from pathlib import Path

context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
SECRECT_KEY = setting.SECRECT_KEY
ALGORITHM = "HS256"
sequrity = HTTPBearer()

# hashing password --->

def hash_password(password:str): #takes a pass given by user 
    return context.hash(password)

#verifying hashed passsword --->

def verify_password(plain_password:str , hashed_password:str): #take plain pass and compaire with hashed one when login 
    return context.verify( plain_password,hashed_password ,)    

# creating tocken ---->

def create_token(email:str , id:str):
    now = datetime.now(timezone.utc)
    expire = now+timedelta(minutes=30)
    payload = {
        "sub": id,
        "email":email,
        "exp":expire
    }

    token = jwt.encode(payload , SECRECT_KEY , algorithm=ALGORITHM)
    return token


# verifying token ---->

def verify_token(token:HTTPAuthorizationCredentials =  Depends(sequrity)):
    credential_exception =HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail=  "unautorised " ,
            headers={"www-Authenticate":"Bearer"})
    
    try:
         payload = jwt.decode(token.credentials , SECRECT_KEY , algorithms=[ALGORITHM])
         id = payload.get("sub")
         actual_id = int(id)
         email = payload.get("email")

    except JWTError :
        raise credential_exception

    return {"id":actual_id , "email" : email} 
          
                
# file encryption using AES-GCM --->

def encrypt_file(file_path : str , output_path : str , Key : bytes):
    aesgcm = AESGCM(Key)
    nonce = os.urandom(12)

    with open(file_path,"rb") as f :
        plain_text = f.read()


    cheaper_text = aesgcm.encrypt(nonce , plain_text , associated_data=None)

    with open(output_path , "wb") as f:
        f.write(nonce + cheaper_text)    
              
    
def decrypt_file(file_path:str , output_path : str , key : bytes):
    aesgcm = AESGCM(key)
    with open(file_path , "rb") as f:
        encripted_data = f.read()

    nonce = encripted_data[:12]
    chiper_tex = encripted_data[12:]

    decripted_data = aesgcm.decrypt(nonce , chiper_tex , associated_data=None)  

    with open(output_path , "wb") as f:
        f.write(decripted_data)  



def delet_download_file(path:str):
    try:
        file_path = Path(path)
        if file_path.exists():
            os.remove(file_path)
    except:
             raise HTTPException (401  ,"deleting file error ")   
