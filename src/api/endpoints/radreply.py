from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.db.database import get_db
from src.models.radreply import RadReply
from src.schemas.radreply import RadReplySchema, RadReplyCreate

router = APIRouter()


@router.get("/reply/", response_model=List[RadReplySchema])
def get_radreply_list(
    username: Optional[str] = Query(None, description="Filter by username"),
    attribute: Optional[str] = Query(None, description="Filter by attribute"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(RadReply)

    if username:
        query = query.filter(RadReply.username == username)
        result = query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"User {username} not found"
            )
        return result

    if attribute:
        query = query.filter(RadReply.attribute == attribute)
        result = query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Attribute {attribute} not found"
            )
        return result

    return query.offset(skip).limit(limit).all()


@router.post("/reply/", response_model=RadReplySchema)
def create_radreply(radreply: RadReplyCreate, db: Session = Depends(get_db)):
    db_radreply = RadReply(
        username=radreply.username,
        attribute=radreply.attribute,
        op=radreply.op,
        value=radreply.value
    )
    db.add(db_radreply)
    db.commit()
    db.refresh(db_radreply)
    return db_radreply


@router.put("/reply/{reply_id}", response_model=RadReplySchema)
def update_radreply(reply_id: int, radreply: RadReplyCreate, db: Session = Depends(get_db)):
    db_radreply = db.query(RadReply).filter(RadReply.id == reply_id).first()
    if db_radreply is None:
        raise HTTPException(status_code=404, detail="RadReply not found")

    db_radreply.username = radreply.username
    db_radreply.attribute = radreply.attribute
    db_radreply.op = radreply.op
    db_radreply.value = radreply.value

    db.commit()
    db.refresh(db_radreply)
    return db_radreply


@router.delete("/reply/{reply_id}")
def delete_radreply(reply_id: int, db: Session = Depends(get_db)):
    db_radreply = db.query(RadReply).filter(RadReply.id == reply_id).first()
    if db_radreply is None:
        raise HTTPException(status_code=404, detail="RadReply not found")

    db.delete(db_radreply)
    db.commit()
    return {"message": "RadReply deleted successfully"}
