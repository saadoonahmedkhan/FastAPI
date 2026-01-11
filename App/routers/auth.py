from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2
from ..schema import Post, User_login
from .. import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    tags = ["Authentication"]
    )

@router.post("/login",status_code=status.HTTP_200_OK)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    if user_credentials.username == "" or user_credentials.username is None or user_credentials.password == "" or user_credentials.password is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Invalid Credentials")
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    verified = utils.verify(user_credentials.password,user.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"sub":str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}