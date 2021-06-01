from logging import FATAL
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, responses, status, Response
from . import schemas, models
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = models.Blog(title=request.title, body=request.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id}')
  blog.delete(synchronize_session=False)
  db.commit()
  return {'Blog removido com sucesso'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).update(
      {request.title, request.body})
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id}')
  db.commit()
  return {'Blog atualizado com sucesso'}


@app.get('/blog')
def all(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).all()
  return blogs


@app.get('/blog/{id}', status_code=200)
def show(id, response: Response, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with the id {id} is not available.')
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'detail': f'Blog with the id {id} is not available.'}

  return blog
