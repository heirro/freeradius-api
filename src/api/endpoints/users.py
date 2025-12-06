from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models.radcheck import RadCheck
from src.models.radreply import RadReply
from src.schemas.radcheck import RadCheckCreate, RadCheckSchema

router = APIRouter()


@router.get("/users", response_model=List[RadCheckSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(RadCheck).all()
    return users


@router.get("/users/{username}", response_model=List[RadCheckSchema])
def get_user(username: str, db: Session = Depends(get_db)):
    users = db.query(RadCheck).filter(RadCheck.username == username).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found"
        )
    return users


@router.post("/users", response_model=RadCheckSchema)
def create_user(user: RadCheckCreate, db: Session = Depends(get_db)):
    db_user = RadCheck(
        username=user.username,
        attribute=user.attribute,
        op=user.op,
        value=user.value
    )

    db.add(db_user)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=List[RadCheckSchema])
async def update_user(
    user_id: int,
    user: RadCheckCreate = Body(...),
    db: Session = Depends(get_db)
):
    try:
        db_users = db.query(RadCheck).filter(RadCheck.id == user_id).all()
        if not db_users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found"
            )

        for db_user in db_users:
            db_user.username = user.username
            db_user.attribute = user.attribute
            db_user.op = user.op
            db_user.value = user.value

        db.commit()
        for db_user in db_users:
            db.refresh(db_user)
        return db_users
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(RadCheck).filter(RadCheck.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    db_radreply = db.query(RadReply).filter(
        RadReply.username == db_user.username,
        RadReply.attribute == "Framed-Pool",
    ).first()

    if db_radreply:
        db.delete(db_radreply)

    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}
