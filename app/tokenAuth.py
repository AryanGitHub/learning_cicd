from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session


from datetime import datetime , timedelta , timezone

from .database import get_db
from . import models , config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET = config.settings.secret
ALGORITHM = "HS256"
TIMEOUT_TOKEN_MINUTES = config.settings.token_timeout_minutes

"""
A user info structure
{
    "username": "<A username>" ,
    "exp" : "<A timestamp to get this token expired>"
}

"""

def generate_token(userInfo : dict):
    expire = datetime.now(timezone.utc) + timedelta(minutes=TIMEOUT_TOKEN_MINUTES)
    userInfo.update({"exp": expire})
    generated_token = jwt.encode(userInfo, SECRET, algorithm=ALGORITHM)
    return generated_token

def verify_token_and_get_username_from_token(userToken : dict , InvalidTokenError):
    try:
        user = jwt.decode(userToken, SECRET, algorithms=[ALGORITHM])
        username = user["username"]
        if not username:
            raise InvalidTokenError
        return username
    except JWTError:
        raise InvalidTokenError
    
def validate_token_and_return_user_from_db( token : str = Depends (oauth2_scheme) , db : Session = Depends(get_db)):
    InvaildTokenError = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    username = verify_token_and_get_username_from_token(token , InvaildTokenError)
    user = db.query(models.user).filter(username == models.user.username).first()
    if not user :
        raise InvaildTokenError
    return user

