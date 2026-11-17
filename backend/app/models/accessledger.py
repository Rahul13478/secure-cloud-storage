from app.db.base import Base
from sqlalchemy import Column , Integer , String , ForeignKey, DateTime , func

from app.models.user import User
from app.models.files import File

class AccessLedger(Base):
    __tablename__  =  "access_ledger"
    id = Column(Integer , primary_key=True)
    event_type = Column(String)
    user_id = Column(Integer , ForeignKey(User.id))
    file_id  = Column(Integer )
    timestamp = Column(DateTime(timezone=True) , server_default=func.now())
    previous_hash = Column(String)
    block_hash = Column(String)
