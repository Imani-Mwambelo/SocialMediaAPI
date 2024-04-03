from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter

from sqlalchemy.orm import Session
from sqlalchemy import func

from app import oauth2
from .. import models, schemas, utils
from ..database import engine, get_db

router=APIRouter(tags=['Posts'])

@router.get("/posts", response_model=list[schemas.PostOut])
def get_posts(db: Session=Depends(get_db), user_id=Depends(oauth2.get_current_user), limit:int=10, skip:int=0, search:Optional[str]=""):

    # cursor.execute("SELECT * FROM posts")
    # posts=cursor.fetchall() 
    posts_query=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id)
    posts=posts_query.all()

    return posts


@router.post("/posts", response_model=schemas.Post)
def create_post(post:schemas.PostCreate, db: Session=Depends(get_db), user_id=Depends(oauth2.get_current_user)):
    # 
    
    new_post=models.Post(owner_id=user_id, **post.model_dump()) 
    #new_post['owner_id']=user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}",response_model=schemas.PostOut)
def get_post(id:int, db: Session=Depends(get_db), user_id=Depends(oauth2.get_current_user)):
    # post=find_post(id)
    print(user_id)
    posts_query=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id)
    post=posts_query.first()

    #post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} do not exist")
        
    return post
    
@router.delete("/posts/{id}")
def delete_post(id: int, db: Session=Depends(get_db), user_id=Depends(oauth2.get_current_user)):
    #print(user_id)
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
     #cursor.execute("DELETE FROM posts WHERE id=%s  returning *", (id,))
     #post=cursor.fetchone()
     #conn.commit()
    
       
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} do not exist")

    if post.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action") 
    post_query.delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"post with id {id} was successfully deleted")
    
        
@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate, db: Session=Depends(get_db), user_id=Depends(oauth2.get_current_user)):
    print(user_id)
    # cursor.execute("UPDATE posts SET title= %s, content=%s, published=%s WHERE id=%s RETURNING *", (post.title, post.content,post.published,id))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    updated_post=post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} do not exist")
    
    if updated_post.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action") 
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post
