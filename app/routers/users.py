from .. import models, schemas, utils
from typing import Optional
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserOut

from random import randint

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate ,db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db),):
    user_query = db.query(models.User).filter(models.User.id == id).first()
    
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} not found")

    return  user_query

