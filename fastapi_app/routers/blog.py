from fastapi import APIRouter, Depends, status
from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)
get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = models.Blog(title=request.title, body=request.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id}')
  blog.delete(synchronize_session=False)
  db.commit()
  return {'Blog removido com sucesso'}


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).update(
      {request.title, request.body})
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id}')
  db.commit()
  return {'Blog atualizado com sucesso'}


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with the id {id} is not available.')
  return blog
