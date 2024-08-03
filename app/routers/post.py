from .. import models, schemas, utils
from  .. import oauth2

from typing import Optional, List
from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter

from  ..schemas import Post, CreatePost ,PostResponse,PostOut
from ..database import  get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

from random import randint

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)




# @router.get('/', response_model=List[schemas.PostResponse])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user), limit: int  = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    # print(posts)
    response = [
        {"post": (post), "votes": votes}
        for post, votes in results
    ]
    return response



@router.post('/', status_code=status.HTTP_201_CREATED,  response_model=schemas.PostResponse)
def create_posts(new_post: CreatePost, db: Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):
    # staged changes but not commited
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """,
    #                (new_post.title, new_post.content, new_post.published))
    # my_new_post = cursor.fetchone()
    # committing the changes

    # my_new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    my_new_post = models.Post(owner_id= current_user.id ,**new_post.model_dump())


    

    # conn.commit()
    print(current_user.email)
    db.add(my_new_post)
    db.commit()
    db.refresh(my_new_post)

    return my_new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session =  Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()
    # print(post)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found")

        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post {id} not found"}
    post, votes = result


    response_data = {
        "post": post,  
        "votes": votes
    }

    return response_data

@router.put('/{id}', response_model=schemas.PostResponse)
def update_posts(id: int, new_post: Post, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (new_post.title, new_post.content, new_post.published, str(id)))

    # updated_post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested actions")
    # post_dict = new_post.model_dump()
    # post_dict['id'] = id
    # my_post[index] = post_dict

    # post_query.update({'title': "this is a post", 'content': 'this is post content'}, synchronize_session=False)
    post_query.update(new_post.model_dump() ,synchronize_session=False)

    db.commit()

    return post_query.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """ DELETE FROM posts WHERE id = %s  RETURNING * """, (str(id),))

    # deleted_post = cursor.fetchone()

    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested actions")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # title: str, content: str, category: str
