from fastapi import FastAPI
from typing import Optional

import pydantic

app = FastAPI()


@app.get('/')
def index(limit=10, published: bool = True, sort: Optional[str] = None):
  # get only {limit} blogs
  if published:
    return {'data': f'{limit} published blogs from de DataBase'}
  else:
    return {'data': f'{limit} blogs from de DataBase'}


@app.get('/about')
def about():
  return {'data': 'about page'}


# Rotas sem parametros devem vir primeiro, para nao quebrar na conversao


@app.get('/blog/unpublished')
def unpublished():
  return {'data': "all unpublished blogs"}


@app.get('/blog/{id}')
def show(id: int):
  # fetch blog with id = id
  return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int, limit=10):
  # fetch comments of blog with id = id
  return {'data': {'1', '2'}}
