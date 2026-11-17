from app.db.base import Base
from app.models.user import User
from sqlalchemy import Column , Integer , String , DateTime , func , ForeignKey ,Boolean

class File(Base):
    __tablename__ = "files"
    id = Column(Integer , primary_key=True)
    owner_id = Column(Integer , ForeignKey(User.id))
    original_filename = Column(String , nullable=False)
    stored_filename = Column(String , nullable=False)
    file_path = Column(String , nullable=False)
    file_size = Column(String , nullable=False)
    content_type = Column(String , nullable=False)
    is_encrypted = Column(Boolean,default=True)
    created_at = Column(DateTime(timezone=True) , server_default= func.now())
    updated_at = Column(DateTime(timezone=True ),server_default = func.now() ,onupdate=func.now())


