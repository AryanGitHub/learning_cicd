from fastapi import HTTPException , Depends, status , APIRouter 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models , schema , utils , tokenAuth

router = APIRouter(prefix="/login" , tags=["Login"])

@router.post("" , response_model=schema.authToken_response)
def get_token_from_credentials( user_credentials_body : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.username == user_credentials_body.username).first()
    invalid_credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"Error: Invalid credentials")
    if (not user) or (not utils.verify_password(user_credentials_body.password , user.password_hashed)):
        raise invalid_credentials_exception
    else :
        user_info = {"username" : user.username}
        token = tokenAuth.generate_token(user_info)
        response = schema.authToken_response(access_token=token)
        return response
    

    
    