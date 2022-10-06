from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote  
from .config import settings

# Code below not needed due to Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#CORS - allows connections from any domain
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Get all users
@app.get("/")
def root():
    return {"message", "Hello World"}
