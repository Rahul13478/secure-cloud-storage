from app.db.base import Base
from app.models.user import User
from sqlalchemy import Column , Integer ,ForeignKey , String , DateTime , func

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableList

class Face(Base):
    __tablename__ = "face_profiles"
    id = Column(Integer , primary_key=True)
    user_id  = Column(Integer ,ForeignKey(User.id) , unique=True , nullable=False )
    embedding   = Column(MutableList.as_mutable(JSON),  nullable=False)
    model_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),  server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
