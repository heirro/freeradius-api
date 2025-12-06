from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from src.db.database import get_db
from src.models.radgroupreply import RadGroupReply
from src.schemas.radgroupreply import RadGroupReplySchema, RadGroupReplyCreate

router = APIRouter()

class GroupSearch(BaseModel):
    groupname: str

@router.get("/group/", response_model=List[RadGroupReplySchema])
def get_radgroupreply_list(
    name: Optional[str] = Query(None, description="Filter by group name"),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    query = db.query(RadGroupReply)
    
    if name:
        query = query.filter(RadGroupReply.groupname == name)
        result = query.all()
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"Group Name {name} not found"
            )
        return result
    
    return query.offset(skip).limit(limit).all()


@router.post("/group/", response_model=RadGroupReplySchema)
def create_radgroupreply(radgroupreply: RadGroupReplyCreate, db: Session = Depends(get_db)):
    db_radgroupreply = RadGroupReply(
        groupname=radgroupreply.groupname,
        attribute=radgroupreply.attribute,
        op=radgroupreply.op,
        value=radgroupreply.value
    )
    db.add(db_radgroupreply)
    db.commit()
    db.refresh(db_radgroupreply)
    return db_radgroupreply

@router.put("/group/{group_id}", response_model=RadGroupReplySchema)
def update_radgroupreply(group_id: int, radgroupreply: RadGroupReplyCreate, db: Session = Depends(get_db)):
    db_radgroupreply = db.query(RadGroupReply).filter(RadGroupReply.id == group_id).first()
    if db_radgroupreply is None:
        raise HTTPException(status_code=404, detail="RadGroupReply not found")
    
    # Update attributes
    db_radgroupreply.groupname = radgroupreply.groupname
    db_radgroupreply.attribute = radgroupreply.attribute
    db_radgroupreply.op = radgroupreply.op
    db_radgroupreply.value = radgroupreply.value
    
    db.commit()
    db.refresh(db_radgroupreply)
    return db_radgroupreply

@router.delete("/group/{group_id}")
def delete_radgroupreply(group_id: int, db: Session = Depends(get_db)):
    db_radgroupreply = db.query(RadGroupReply).filter(RadGroupReply.id == group_id).first()
    if db_radgroupreply is None:
        raise HTTPException(status_code=404, detail="RadGroupReply not found")
    
    db.delete(db_radgroupreply)
    db.commit()
    return {"message": "RadGroupReply deleted successfully"} 