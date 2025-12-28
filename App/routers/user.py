from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils
from ..schema import User, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


# User Endpoints
@router.get("", status_code=status.HTTP_200_OK, response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
def get_userById(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: User, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, updated_user: User, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    existing_user = user_query.first()
    if existing_user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} does not exist."
        )

    updated_data = updated_user.model_dump()
    user_query.update(
        {
            "username": updated_data["username"],
            "email": updated_data["email"],
            "password": updated_data["password"],
        },
        synchronize_session=False,
    )
    db.commit()
    return {"message": "User updated successfully"}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} does not exist."
        )
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
