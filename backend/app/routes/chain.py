from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.blockchain.blockchain import verify_chain

router = APIRouter(prefix="/chain",tags=["Chain"])

@router.post("/chain")
def call_chain(db : Session = Depends(get_db) ):
    result = verify_chain(db)
    return result
