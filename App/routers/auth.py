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
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    verified = utils.verify(user_credentials.password,user.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"sub":str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}