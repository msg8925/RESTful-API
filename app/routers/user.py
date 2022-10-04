from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import engine, get_db
from ..schemas import User, UserCreate
from ..utils import hash

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# Get all users
@router.get("/", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


# Get a single user
@router.get("/{id}", response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with id: {id} not found")
    
    return user


# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    user.password = hash(user.password)

    # The line below is able to replace the longer line below it 
    new_user = models.User(**user.dict())
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Update a user
@router.put("/{id}", response_model=User)
def update_user(id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user_query.first()

    if user_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} doesn't exist.")
    
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()


# Delete a user
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} not found.")

    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)