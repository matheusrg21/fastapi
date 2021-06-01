from logging import FATAL
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, responses, status, Response
from typing import List
from passlib.context import CryptContext
from . import schemas, models
from .database import SessionLocal, engine
from .hash import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = models.Blog(title=request.title, body=request.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id}')
  blog.delete(synchronize_session=False)
  db.commit()
  return {'Blog removido com sucesso'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).update(
      {request.title, request.body})
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id}')
  db.commit()
  return {'Blog atualizado com sucesso'}


@app.get('/blog', response_model=List[schemas.ShowBlog], tags=["blogs"])
def all(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
def show(id: int, response: Response, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with the id {id} is not available.')
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f'Blog with the id {id} is not available.'}

  return blog


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
  new_user = models.User(
      name=request.name, email=request.email, password=Hash.bcrypt(request.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return request


@app.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'User with the id {id} is not available.')

  return user
