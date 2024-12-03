from fastapi import HTTPException , Depends, status , APIRouter 
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models , schema
from .. import tokenAuth


router = APIRouter(prefix="/posts" , tags=["Resource Posts"])

@router.get("/all" ,response_model=List[schema.resource_post_response3]) 
def get_all_post(db : Session = Depends(get_db)):
    sub_query = db.query(models.vote.post_id , func.sum(models.vote.vote).label("votes")).group_by(models.vote.post_id).subquery()
#   all_posts_query = db.query(models.resource , models.resource.votes.label("unwanted_filed")).join(sub_query , models.resource.post_id == sub_query.columns.post_id).limit(5)
    all_posts_query = (
    db.query(models.resource.post_id , models.resource.title, models.resource.description , models.resource.http_link ,models.resource.author_id, models.resource.created_at , sub_query.c.votes)
    .join(sub_query, models.resource.post_id == sub_query.c.post_id))
    all_posts = all_posts_query.all()
    return all_posts
    


@router.get("" ,response_model=List[schema.resource_post_response]) 
def get_all_post(db : Session = Depends(get_db) , user : schema.user_response = Depends(tokenAuth.validate_token_and_return_user_from_db)):
    all_posts = db.query(models.resource).all()
    return all_posts


@router.get("/{id}" , response_model=schema.resource_post_response2)
def get_post_with_id(id : int , db : Session = Depends(get_db), user : schema.user_response = Depends(tokenAuth.validate_token_and_return_user_from_db)):
    post = db.query(models.resource).filter(models.resource.post_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
        detail=f" ID {id} Not Found.")
    return post


@router.post("" , status_code=status.HTTP_201_CREATED , response_model=schema.resource_post_response2)    
def create_posts( post_body :schema.resource_post_create , db : Session = Depends(get_db), user : schema.user_response = Depends(tokenAuth.validate_token_and_return_user_from_db)):
    new_post = models.resource(author_id=user.user_id,**post_body.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db : Session = Depends(get_db), user : schema.user_response = Depends(tokenAuth.validate_token_and_return_user_from_db)):
    post_query = db.query(models.resource).filter(models.resource.post_id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No post with id {id} found")
    if user.user_id != post.author_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Not Authorized for this request.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return None
    

@router.put("/{id}" , response_model=schema.resource_post_response2)
def update_post(id : int, new_post_body : schema.resource_post_create ,  db : Session = Depends(get_db) , user : schema.user_response = Depends(tokenAuth.validate_token_and_return_user_from_db)):
    post_query = db.query(models.resource).filter(models.resource.post_id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No post with id {id} found")
    if user.user_id != post.author_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Not Authorized for this request.")
    to_add = new_post_body.model_dump()
    to_add["author_id"] = user.user_id
    to_add["post_id"] = post.post_id

    post_query.update(to_add,synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post


