from pydantic import BaseModel

class otp_input(BaseModel):
    email : str
    otp : str

class resend_otp_input(BaseModel):
    email: str