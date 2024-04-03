from fastapi import status, HTTPException,Depends, APIRouter

from sqlalchemy.orm import Session

from app import oauth2
from .. import models, schemas, utils
from ..database import  get_db


router= APIRouter( tags=['Vote'])


@router.post('/vote', status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session=Depends(get_db), user_id=Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} does not exist")

    

    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==user_id)
    found_vote=vote_query.first()

    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"the user {user_id} has already voted for this post")
        new_vote=models.Vote(post_id=vote.post_id, user_id=user_id)
        db.add(new_vote)
        db.commit()
        return{"message":"successfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"successfully deleted vote"}

      


     



