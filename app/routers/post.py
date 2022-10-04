from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import engine, get_db
from ..schemas import PostCreate, Post
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Get all posts
@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
 

# Get all posts from currently logged in user
@router.get("/user", response_model=List[Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


# Get a single post
@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} not found")
    
    return post


# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    # Convert 'post' from request to a dict, then unpack the dict and create a 'Post' model object and finally store it in 'new_post'  
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    
    # Insert new post into DB
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


# Update a post
@router.put("/{id}", response_model=Post)
def update_post(id: int, post:PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_db = post_query.first()

    # Check that the post exists
    if post_db == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist.")
    

    # Check if it's the owner trying to update the post
    if post_db.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this action") 

    # Update the post
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


# Delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Check that the post exists
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found.")

    # Check if it's the owner trying to delete the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this action") 

    # Delete the post
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
