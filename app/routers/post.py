
from typing import Optional
from fastapi import Depends, FastAPI,Response,status,HTTPException,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models,schemas,oauth
from .. database import get_db,engine



router = APIRouter(
    prefix = '/posts',
    tags = ['Posts']
)
my_posts = [{"title" : "post 1","content" : "content one", "id" : 1},{'title' : "post 2","content" : "content two", "id" : 2},{'title' : "post 3","content" : "content three", "id" : 3},{'title' : "post 4","content" : "content four", "id" : 4}]


# @router.get('/',response_model=list[schemas.Post])
@router.get('/',response_model=list[schemas.PostOut])
def get_post(db:Session = Depends(get_db),current_user :int= Depends(oauth.get_current_user),
limit:int = 10,skip:int = 0, search:Optional[str] = ""):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    post = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return post
    # print(posts)
    # return posts 


@router.post('/', status_code= status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(new_post : schemas.PostCreate,db:Session = Depends(get_db),user_id :int= Depends(oauth.get_current_user)):
    # cursor.execute(""" INSERT INTO posts(title,content,published) VALUES (%s,%s,%s)  RETURNING * """,(new_post.title,new_post.content,new_post.published))
    # neww_posts = cursor.fetchone()
    # conn.commit()

    # new_created_post = models.Post(title = new_post.title,content = new_post.content,published = new_post.published)
    print(user_id.email)
    new_created_post = models.Post(owner_id = user_id.id,**new_post.dict())
    db.add(new_created_post)
    db.commit()
    db.refresh(new_created_post)
    return new_created_post     

 

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session = Depends(get_db),user_id :int= Depends(oauth.get_current_user)):
    # cursor.execute(""" select * from posts where id = %s""",(str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id == models.Post.id,isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=  f"post with id : {id} was not found!")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id : {id} not found!"}
    return post   



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user :int= Depends(oauth.get_current_user)):
    # index = find_index(id)
   
    # cursor.execute(""" delete from posts where id = %s returning * """,(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= {'message' : f" post with id {id} does not exists."})

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to permorm the requested operations!")     

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id:int,updated_post:schemas.PostCreate,db:Session = Depends(get_db),current_user :int= Depends(oauth.get_current_user)):
    # print(post)

    # cursor.execute(""" update posts set title = %s,content = %s,published = %s where id = %s returning * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail= {'message' : f" post with id {id} does not exists."})
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to permorm the requested operations!") 

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit() 
    return post_query.first()


