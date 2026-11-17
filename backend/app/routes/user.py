from fastapi import APIRouter , Depends , BackgroundTasks , HTTPException , Request , status
from app.schemas.users import UserRegister , UserLogin
from app.schemas.otpschema import otp_input , resend_otp_input
from app.otp.otp import generate_otp
import secrets
from app.dna.dna import  dna_make
from app.models.user import User
from app.db.database import get_db
from sqlalchemy.orm import Session 
from app.security.auth import hash_password , verify_password , create_token
from app.email.sentemail import send_dna , send_otp
from redis.asyncio import Redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.rate_limit.rate_limit import read_count , test_rate_limit , clear_count
from app.file_storage_cloud.s3_storage import bucket_create
router = APIRouter(prefix="/users",tags=["Users"])
@asynccontextmanager
async def Lifespan(app:FastAPI):
    app.state.redis = Redis.from_url("redis://localhost:6379",decode_responses = True )
    yield
    await app.state.redis.close()
bucket_create()    

# register users ---->

@router.post("/register" , status_code=status.HTTP_201_CREATED)
def user_register(user:UserRegister, background : BackgroundTasks, db : Session = Depends(get_db) ):
    token  = secrets.token_hex(16) 
    genereted_dna = dna_make(token)
    hashed = hash_password(user.password)
    new_user = User(name = user.name ,
                     email = user.email ,
                       password_hash = hashed ,
                        phone_number = user.phone_number,
                         user_name = user.user_name,
                         secret_code = token,
                         dna_sequence = genereted_dna,
                         role = "user")

    background.add_task(send_dna , user , genereted_dna)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


   
    return {"message":"user registerd successfully"}

    
# user login ---->
# email/password check
# ↓
# take stored secret_code
# ↓
# regenerate DNA
# ↓
# compare with stored dna_sequence
# ↓
# generate otp --> make connection with redis (lifespan ,asyncontexmaneger)-->put it in main.py fastapi --> generate otp in login ---> save it in redis with key and value pair --> then verify otp route
# ↓
# comapre with redis otp
# ↓
# login


#user login ----->   
# puting rate limit count only faild attemts  
#  a user can only use 5 pass for each acc only for 1 minit 
# best is use both per ip and per acc

#

@router.post("/login")
async def user_login(user:UserLogin , request:Request, background:BackgroundTasks, db : Session = Depends(get_db)):

    get_user = db.query(User).filter_by(email = user.email).first()
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_id = get_user.id
    str_user_id =str(user_id)
    user_email = user.email
    key = "Login_fail:"+user_email
    key_for_login = "login_ok:"+user_email

  
    read = read_count(key , 5)
    if read is True:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    

    cheack_password = verify_password(plain_password=user.password , hashed_password=get_user.password_hash)

    if cheack_password == False:
        test_rate_limit(key , 5 , 120)
        raise HTTPException(401 , "wrong password ")
    
    if cheack_password == True:
        

        token = get_user.secret_code
        remake_dna = dna_make(token)

        if remake_dna != user.dna:
            test_rate_limit(key , 5 ,120)
            raise HTTPException(401 , "wrong DNA")   
        
        if remake_dna == user.dna:
            clear_count(key)
            otp = generate_otp()
            background.add_task(send_otp, user , otp)
            await request.app.state.redis.set(user.email , otp , ex =120 )
            await request.app.state.redis.set(key_for_login , 1  , ex = 900)

            
        return  {"message":"otp send successfully"}   

#i can return this toke after otp verify because i get email from frontend and get_user to id 
#should i do that i dont know :)
#otp verification-----> i will change it letter 

@router.post("/otp_verify")
async def otp_verifivation(data:otp_input , request : Request , db : Session = Depends(get_db) ):
    key_for_login = "login_ok:"+data.email
    key = "otp_fail:"+ data.email
    read = read_count(key , 5)
    if read  is True:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    retrive_otp = await request.app.state.redis.get(data.email)
    if retrive_otp != data.otp:
        test_rate_limit(key , 5 , 180 )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if retrive_otp == data.otp:
        clear_count(key)  
        await request.app.state.redis.delete(data.email)  
        await request.app.state.redis.delete(key_for_login)
        get_user = db.query(User).filter_by(email = data.email).first()
        user_id = get_user.id
        str_user_id = str(user_id)
        jwt_token = create_token(data.email , str_user_id)

    return jwt_token    

# need to make ip limiter 
# need to make resend otp with a limit of 5 chanhce in 15 minits 
#qr for face verify 

@router.post("/resend-otp")
async def resend_otp(data:resend_otp_input ,request : Request ,background:BackgroundTasks ,   db:Session = Depends(get_db)):
    key_for_login = "login_ok:"+data.email
    
    login_ok_exists = await request.app.state.redis.exists(key_for_login)

    if login_ok_exists > 0 :
         
        key = "otp_resend:"+data.email
        read = read_count(key , 5 )
            
        if read is True:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
            
        exists_count = await request.app.state.redis.exists(data.email)
            
        if exists_count > 0 :
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
            
        otp = generate_otp()
            
        background.add_task(send_otp , data , otp)
            
        await request.app.state.redis.set(data.email , otp , ex=120)
            
        test_rate_limit(key , 5 , 900)
        
            
        return {"message":"otp send successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
         
    

