from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from src.db.database import get_db
from src.models.nas import NAS
from src.schemas.nas import NAS as NASSchema, NASCreate

router = APIRouter()


@router.get("/nas/", response_model=List[NASSchema])
def get_nas_list(
    nasname: Optional[str] = Query(None, description="Filter by NAS name"),
    type: Optional[str] = Query(None, description="Filter by NAS type"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(NAS)
    
    if nasname:
        query = query.filter(NAS.nasname == nasname)
        result = query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"NAS with name {nasname} not found"
            )
        return result
    
    if type:
        query = query.filter(NAS.type == type)
        result = query.all()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"NAS with type {type} not found"
            )
        return result
    
    return query.offset(skip).limit(limit).all()


@router.get("/nas/{nas_id}", response_model=NASSchema)
def get_nas(nas_id: int, db: Session = Depends(get_db)):
    nas = db.query(NAS).filter(NAS.id == nas_id).first()
    if nas is None:
        raise HTTPException(status_code=404, detail="NAS not found")
    return nas

@router.post("/nas/", response_model=NASSchema)
def create_nas(nas: NASCreate, db: Session = Depends(get_db)):
    db_nas = NAS(
        nasname=nas.nasname,
        shortname=nas.shortname,
        type=nas.type,
        ports=nas.ports,
        secret=nas.secret,
        server=nas.server,
        community=nas.community,
        description=nas.description
    )
    db.add(db_nas)
    db.commit()
    db.refresh(db_nas)
    return db_nas


@router.put("/nas/{nas_id}", response_model=NASSchema)
def update_nas(nas_id: int, nas: NASCreate, db: Session = Depends(get_db)):
    db_nas = db.query(NAS).filter(NAS.id == nas_id).first()
    if db_nas is None:
        raise HTTPException(status_code=404, detail="NAS not found")
    
    # Update attributes
    db_nas.nasname = nas.nasname
    db_nas.shortname = nas.shortname
    db_nas.type = nas.type
    db_nas.ports = nas.ports
    db_nas.secret = nas.secret
    db_nas.server = nas.server
    db_nas.community = nas.community
    db_nas.description = nas.description
    
    db.commit()
    db.refresh(db_nas)
    return db_nas


@router.delete("/nas/{nas_id}")
def delete_nas(nas_id: int, db: Session = Depends(get_db)):
    db_nas = db.query(NAS).filter(NAS.id == nas_id).first()
    if db_nas is None:
        raise HTTPException(status_code=404, detail="NAS not found")
    
    db.delete(db_nas)
    db.commit()
    return {"message": "NAS deleted successfully"} 