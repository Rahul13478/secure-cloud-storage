from fastapi_mail import FastMail  , MessageSchema , MessageType , ConnectionConfig
from app.schemas.users import UserRegister , UserLogin
from app.core.settings import setting

conf = ConnectionConfig(
    MAIL_USERNAME=setting.EMAIL_SENDER,
    MAIL_PASSWORD=setting.EMAIL_PASSWORD,#get from app password in google acc in email
    MAIL_FROM=setting.EMAIL_SENDER,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_dna(user:UserRegister , dna:str):
        messege = MessageSchema(
          subject=f"Welcome {user.name} here is your dna",
          recipients=[user.email],
          body=dna,
          subtype=MessageType.html
    )
        fn = FastMail(conf)
        await fn.send_message(messege)


async def send_otp(user:UserLogin , otp:str):
        messege = MessageSchema(
                subject="this is your otp",
                recipients=[user.email],
                body=otp,
                subtype=MessageType.html
        )   
        fn = FastMail(conf)
        await fn.send_message(messege) 
