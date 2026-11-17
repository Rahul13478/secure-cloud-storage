from app.db.base import Base
from sqlalchemy import Column , Integer , String ,Boolean,   DateTime , func

class User(Base):
    __tablename__ = "users"
    id  = Column(Integer , primary_key=True)
    name = Column(String , nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String , nullable=True)
    user_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    dna_sequence = Column(String, nullable=False)
    secret_code = Column(String)
    role = Column(String,nullable=False)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), server_default= func.now(), onupdate=func.now())
