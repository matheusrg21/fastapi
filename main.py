from fastapi import FastAPI
import pydantic

app = FastAPI()


@app.get('/')
def index():
  return {'data': 'Blog list'}


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
def comments(id: int):
  # fetch comments of blog with id = id
  return {'data': {'1', '2'}}
