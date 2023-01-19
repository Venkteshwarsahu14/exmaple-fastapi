from typing import Optional
from fastapi import Depends, FastAPI,Response,status,HTTPException,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
import time
from .. import models,utils,schemas
from .. database import get_db,engine

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/",status_code= status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(new_user : schemas.UserCreate,db:Session = Depends(get_db)):
    hashed_password = utils.hash(new_user.password)
    new_user.password = hashed_password
    new_created_user = models.User(**new_user.dict())
    db.add(new_created_user)
    db.commit()
    db.refresh(new_created_user)
    return new_created_user  

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id = {id} does not exists!')
    return user