from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from src.db.database import get_db
from src.models.radgroupcheck import RadGroupCheck
from src.schemas.radgroupcheck import RadGroupCheckSchema, RadGroupCheckCreate

router = APIRouter()

class GroupSearch(BaseModel):
    groupname: str

@router.get("/group-check/", response_model=List[RadGroupCheckSchema])
def get_radgroupcheck_list(
    name: Optional[str] = Query(None, description="Filter by group name"),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    query = db.query(RadGroupCheck)
    
    if name:
        query = query.filter(RadGroupCheck.groupname == name)
        result = query.all()
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"Group Name {name} not found"
            )
        return result
    
    return query.offset(skip).limit(limit).all()


@router.post("/group-check/", response_model=RadGroupCheckSchema)
def create_radgroupcheck(radgroupcheck: RadGroupCheckCreate, db: Session = Depends(get_db)):
    db_radgroupcheck = RadGroupCheck(
        groupname=radgroupcheck.groupname,
        attribute=radgroupcheck.attribute,
        op=radgroupcheck.op,
        value=radgroupcheck.value
    )
    db.add(db_radgroupcheck)
    db.commit()
    db.refresh(db_radgroupcheck)
    return db_radgroupcheck

@router.put("/group-check/{group_id}", response_model=RadGroupCheckSchema)
def update_radgroupcheck(group_id: int, radgroupcheck: RadGroupCheckCreate, db: Session = Depends(get_db)):
    db_radgroupcheck = db.query(RadGroupCheck).filter(RadGroupCheck.id == group_id).first()
    if db_radgroupcheck is None:
        raise HTTPException(status_code=404, detail="RadGroupCheck not found")
    
    # Update attributes
    db_radgroupcheck.groupname = radgroupcheck.groupname
    db_radgroupcheck.attribute = radgroupcheck.attribute
    db_radgroupcheck.op = radgroupcheck.op
    db_radgroupcheck.value = radgroupcheck.value
    
    db.commit()
    db.refresh(db_radgroupcheck)
    return db_radgroupcheck

@router.delete("/group-check/{group_id}")
def delete_radgroupcheck(group_id: int, db: Session = Depends(get_db)):
    db_radgroupcheck = db.query(RadGroupCheck).filter(RadGroupCheck.id == group_id).first()
    if db_radgroupcheck is None:
        raise HTTPException(status_code=404, detail="RadGroupCheck not found")
    
    db.delete(db_radgroupcheck)
    db.commit()
    return {"message": "RadGroupCheck deleted successfully"}

