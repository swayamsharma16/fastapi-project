from fastapi import FastAPI, Body, Response
from app.routers import vote
from . import models
from .database import engine, get_db
from .routers import post, users, auth
from .config import settings
# setting up cors


import os


from fastapi.middleware.cors import CORSMiddleware



print(settings.database_username)

# the order matters
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# command from sqlalchemy to interact with the database
# models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to my api"}

# test route - sqlalchemy
# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):

#     posts =  db.query(models.Post)
#     print(posts)
#     return {"data": "success"}

# @app.get('/myFunc')
# def myfunc():
#     return {"message": "Welcome inside my function"}



# For local development and testing
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

