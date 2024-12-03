from fastapi import HTTPException , Depends, status , APIRouter 
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models , schema , utils

router = APIRouter(prefix="/users" , tags=["Users"])

@router.post("" ,status_code=status.HTTP_201_CREATED ,response_model=schema.user_response)
def create_user(post_body : schema.user_create , db : Session = Depends(get_db)):
    new_user_dict = post_body.model_dump()
    new_user_dict["password_hashed"] = utils.get_password_hash(post_body.password)
    del new_user_dict["password"]

    # check if username or email already exists
    any_user_with_this_username = db.query(models.user).filter(models.user.username == new_user_dict["username"]).first()
    if any_user_with_this_username:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED , detail= "username already exists")
    any_user_with_this_email = db.query(models.user).filter(models.user.email == new_user_dict["email"]).first()
    if any_user_with_this_email:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED , detail= "email already exists") 

    new_user = models.user(**new_user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/username/{username}" , response_model=schema.user_response)
def get_user_from_username(username : str , db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
        detail=f" Username: {username} Not Found.")
    return user