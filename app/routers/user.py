from fastapi import status, HTTPException,Depends, APIRouter

from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import  get_db

router=APIRouter(tags=['Users'],)


@router.post("/users", response_model=schemas.User)
def create_user(user:schemas.UserCreate, db: Session=Depends(get_db)):
        

        usr=db.query(models.User).filter(models.User.email==user.email).first()
        if not usr:
             
             #Hashing user password
             hashed_password=utils.hash_password(user.password)
             user.password=hashed_password
             new_user=models.User(**user.model_dump())
             db.add(new_user)
             db.commit()
             db.refresh(new_user)
             return new_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"the email already exist, it should be unique")

@router.get("/users/{id}",response_model=schemas.User)
def get_user(id:int, db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} do not exist")
        
    return user

