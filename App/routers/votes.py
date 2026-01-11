from App import schema
from fastapi import APIRouter, Depends, status, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2

router = APIRouter(
    prefix = "/votes",
    tags = ["Votes"]
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {vote.post_id} does not exist")
    if vote.dir == 1:
        found_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).filter(models.Vote.user_id == current_user.id).first()
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    elif vote.dir == 0:
        found_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).filter(models.Vote.user_id == current_user.id).first()
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Vote does not exist")
        db.delete(found_vote)
        db.commit()
        return {"message": "Successfully deleted vote"}
    else:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid vote direction")