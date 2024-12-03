from fastapi import HTTPException , Depends, status , APIRouter 
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models , schema
from .. import tokenAuth

router = APIRouter(prefix="/votes" , tags=["Votes"])

@router.get("/up/{post_id}" ,status_code=status.HTTP_201_CREATED , response_model=schema.vote_response)
def set_upvote_on_post_with_id(post_id : int , db : Session = Depends(get_db), user : schema.user_response = Depends(tokenAuth.validate_token_and_return_user_from_db)):
    post = db.query(models.resource).filter(models.resource.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with id {post_id}, Not Found.")
    # can user preform upvote?
        # no, the following reasons
            # user already did upvote
        # yes , the following reasons
            # user did not cast any vote
            # the user earlier did downvote, so to neutralise or to like, they can upvote
    #---------------------------------------
    #check the vote row for the user
        #if it do not exists, cast the vote.
        #if it exists, 
            #check the upvote number
            # if its -1 or 0, they can upvote , if vote = 0 , delete the row
            # if its 1, then they cant
    vote_with_userID_query = db.query(models.vote).filter(models.vote.post_id == post_id , models.vote.user_id == user.user_id)
    vote_for_user_on_post = vote_with_userID_query.first()
    if not vote_for_user_on_post:
        vote_to_add = models.vote(post_id = post_id , user_id = user.user_id , vote = 1)
        db.add(vote_to_add)
        db.commit()
        db.refresh(vote_to_add)
        response = schema.vote_response(voter_username=user.username, post_id=post_id , vote_status=vote_to_add.vote)
        return response
    else :
        if vote_for_user_on_post.vote == 1:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED , detail=f"Already upvoted. username : {user.username} , post_id : {post_id}")
        else : # vote is rn -1, as upvote it will be 0 and removed from db
            vote_with_userID_query.delete(synchronize_session=False)
            db.commit()
            response = schema.vote_response(voter_username=user.username, post_id=post_id , vote_status=0)
            return response



@router.get("/down/{post_id}" ,status_code=status.HTTP_201_CREATED , response_model=schema.vote_response)
def set_upvote_on_post_with_id(post_id : int , db : Session = Depends(get_db), user : schema.user_response = Depends(tokenAuth.validate_token_and_return_user_from_db)):
    post = db.query(models.resource).filter(models.resource.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with id {post_id}, Not Found.")
    # can user preform downvote?
        # no, the following reasons
            # user already did downvote
        # yes , the following reasons
            # user did not cast any vote
            # the user earlier did upvoted, so to neutralise or to dislike, they can downvote
    #---------------------------------------
    #check the vote row for the user
        #if it do not exists, cast the vote.
        #if it exists, 
            #check the downvote number
            # if its 1 or 0, they can downvote , if vote = 0 , delete the row
            # if its -1, then they cant
    vote_with_userID_query = db.query(models.vote).filter(models.vote.post_id == post_id , models.vote.user_id == user.user_id)
    vote_for_user_on_post = vote_with_userID_query.first()
    if not vote_for_user_on_post:
        vote_to_add = models.vote(post_id = post_id , user_id = user.user_id , vote = -1)
        db.add(vote_to_add)
        db.commit()
        db.refresh(vote_to_add)
        response = schema.vote_response(voter_username=user.username, post_id=post_id , vote_status=vote_to_add.vote)
        return response
    else :
        if vote_for_user_on_post.vote == -1:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED , detail=f"Already downvoted. username : {user.username} , post_id : {post_id}")
        else : # vote is rn 1, as upvote it will be 0 and removed from db
            vote_with_userID_query.delete(synchronize_session=False)
            db.commit()
            response = schema.vote_response(voter_username=user.username, post_id=post_id , vote_status=0)
            return response

