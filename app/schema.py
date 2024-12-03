from datetime import datetime
from pydantic import BaseModel
from typing import Optional 

class resource_post_base (BaseModel):
    post_id : Optional[int] = None
    title : str
    description : Optional[str] = None
    http_link : str
    # tags : dict = {} not_working

class user_base(BaseModel):
    username : str 
    email : str

class resource_post_create (BaseModel):
    title : str
    description : Optional[str] = None
    http_link : str

class resource_post_response (resource_post_base):
    created_at : datetime
    #author_id : int
    author : user_base

class resource_post_response2 (resource_post_base):
    created_at : datetime
    #author_id : int
    author : user_base

class resource_post_response3 (resource_post_base):
    created_at : datetime
    votes: int
    author_id : int


class user_create (user_base):
    password : str

class user_response (user_base):
    user_id : Optional[int] = None
    created_at : datetime

class authToken_response (BaseModel):
    token_type : str = "bearer"
    access_token : str

class vote_response(BaseModel):
    voter_username : str
    post_id : int
    vote_status : int
    