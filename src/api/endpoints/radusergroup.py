from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.db.database import get_db
from src.models.radusergroup import RadUserGroup
from src.schemas.radusergroup import RadUserGroupSchema, RadUserGroupCreate, RadUserGroupUpdate

router = APIRouter()


@router.get("/user-group/", response_model=List[RadUserGroupSchema])
def get_radusergroup_list(
    username: Optional[str] = Query(None, description="Filter by username"),
    groupname: Optional[str] = Query(None, description="Filter by group name"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(RadUserGroup)
    
    if username:
        query = query.filter(RadUserGroup.username == username)
        result = query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"User {username} not found"
            )
        return result
    
    if groupname:
        query = query.filter(RadUserGroup.groupname == groupname)
        result = query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Group {groupname} not found"
            )
        return result
    
    return query.offset(skip).limit(limit).all()


@router.post("/user-group/", response_model=RadUserGroupSchema)
def create_radusergroup(radusergroup: RadUserGroupCreate, db: Session = Depends(get_db)):
    db_radusergroup = RadUserGroup(
        username=radusergroup.username,
        groupname=radusergroup.groupname,
        priority=radusergroup.priority
    )
    db.add(db_radusergroup)
    db.commit()
    db.refresh(db_radusergroup)
    return db_radusergroup


@router.put("/user-group/{group_id}", response_model=RadUserGroupSchema)
def update_radusergroup(group_id: int, radusergroup: RadUserGroupUpdate, db: Session = Depends(get_db)):
    db_radusergroup = db.query(RadUserGroup).filter(RadUserGroup.id == group_id).first()
    if db_radusergroup is None:
        raise HTTPException(status_code=404, detail="RadUserGroup not found")
    
    # Update only groupname
    db_radusergroup.groupname = radusergroup.groupname
    
    db.commit()
    db.refresh(db_radusergroup)
    return db_radusergroup


@router.delete("/user-group/{group_id}")
def delete_radusergroup(group_id: int, db: Session = Depends(get_db)):
    db_radusergroup = db.query(RadUserGroup).filter(RadUserGroup.id == group_id).first()
    if db_radusergroup is None:
        raise HTTPException(status_code=404, detail="RadUserGroup not found")
    
    db.delete(db_radusergroup)
    db.commit()
    return {"message": "RadUserGroup deleted successfully"} 