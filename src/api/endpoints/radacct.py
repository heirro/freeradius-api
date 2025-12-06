from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from sqlalchemy import or_, desc, case
from pydantic import BaseModel

from src.db.database import get_db
from src.models.radacct import RadAcct
from src.models.radcheck import RadCheck
from src.schemas.radacct import RadAcctSchema

router = APIRouter()

class UserStatus(BaseModel):
    username: str
    is_online: bool
    last_session: RadAcctSchema | None = None

@router.get("/", response_model=List[RadAcctSchema])
def get_radacct_list(
    skip: int = 0, 
    limit: int = 100, 
    username: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    query = db.query(RadAcct)
    
    if username:
        query = query.filter(RadAcct.username == username)
    
    if start_date:
        query = query.filter(RadAcct.acctstarttime >= start_date)
    
    if end_date:
        query = query.filter(RadAcct.acctstarttime <= end_date)
    
    # Sort active sessions first, then by start time descending
    query = query.order_by(
        case(
            (or_(
                RadAcct.acctstoptime.is_(None),
                RadAcct.acctstoptime == '0000-00-00 00:00:00'
            ), 0),
            else_=1
        ),
        desc(RadAcct.acctstarttime)
    )
    
    radacct_list = query.offset(skip).limit(limit).all()
    return radacct_list

@router.get("/{radacctid}", response_model=RadAcctSchema)
def get_radacct(radacctid: int, db: Session = Depends(get_db)):
    radacct = db.query(RadAcct).filter(RadAcct.radacctid == radacctid).first()
    if radacct is None:
        raise HTTPException(status_code=404, detail="RadAcct record not found")
    return radacct

# @router.get("/session/{acctsessionid}", response_model=RadAcctSchema)
# def get_radacct_by_session(acctsessionid: str, db: Session = Depends(get_db)):
#     radacct = db.query(RadAcct).filter(RadAcct.acctsessionid == acctsessionid).first()
#     if radacct is None:
#         raise HTTPException(status_code=404, detail="RadAcct session not found")
#     return radacct

@router.get("/status/{username}", response_model=UserStatus)
def get_user_status(username: str, db: Session = Depends(get_db)):
    # Check if user exists in radcheck table
    user = db.query(RadCheck).filter(RadCheck.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found in radcheck table")
    
    # Get the latest session for the user
    latest_session = db.query(RadAcct).filter(
        RadAcct.username == username
    ).order_by(
        desc(RadAcct.acctstarttime)
    ).first()
    
    # If no session found, user is considered offline
    if not latest_session:
        return UserStatus(
            username=username,
            is_online=False,
            last_session=None
        )
    
    # Check if user is online (has active session)
    is_online = latest_session.acctstoptime is None or latest_session.acctstoptime == '0000-00-00 00:00:00'
    
    return UserStatus(
        username=username,
        is_online=is_online,
        last_session=latest_session
    ) 