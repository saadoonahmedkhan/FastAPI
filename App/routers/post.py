from typing import Optional
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models
from ..schema import Post, PostCreate, User, UserOut
from .. import oauth2, utils, schema
from sqlalchemy.orm import aliased

router = APIRouter(prefix="/posts", tags=["Posts"])

# Post Endpoints

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schema.Post_with_Votes])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    results = (
        db.query(
            models.Post,  # full Post object
            func.count(models.Vote.post_id).label("votes")
        )
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) 
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)  # group by post id
        .limit(limit)
        .offset(skip)
        .all()
    )
    if not results:
        raise HTTPException(status_code=404, detail="No posts found")

    return [{"post": post, "votes": votes} for post, votes in results]

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(
    new_post: PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_owner = db.query(models.User).filter(models.User.id == current_user.id).first()
    post = models.Post(
        **new_post.model_dump(), owner=post_owner  # assign the logged-in user
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Post)
def update_post(
    id: int,
    updated_post: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post.",
        )
    updated_data = updated_post.model_dump()
    post_query.update(
        {
            "title": updated_data["title"],
            "content": updated_data["content"],
            "published": updated_data["published"],
        },
        synchronize_session=False,
    )
    db.commit()
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=404, detail=f"Post with id {id} does not exist."
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post.",
        )
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}
