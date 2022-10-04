from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemas import Vote
from ..database import get_db
from ..oauth2 import get_current_user
from .. import models

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    # Check to see if the post that the user is voting on actually exists in the DB
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {vote.post_id} does not exist")

    # Search 'votes' table in DB to see if this vote already exists
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
        
    if vote.dir == 1:
        # Raise an exception if user has already liked the post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        # Create a new vote
        new_vote = models.Vote(user_id=current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message", "successfully added vote"}
    else:
        # Raise an exception if user tries remove a vote that doesn't exist
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User trying to remove a vote that doesn't exist")

        # Remove the vote
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message", "successfully deleted vote"}