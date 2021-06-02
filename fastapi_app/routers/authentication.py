from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_app import database, models, schemas, token
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_app.hash import Hash

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  user = db.query(models.User).filter(
      models.User.email == request.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Invalid credentials for {request.username}')

  if not Hash.verify(user.password, request.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Invalid credentials for {request.username}')

  access_token = token.create_access_token(data={"sub": user.email})

  return {"access_token": access_token, "token_type": "bearer"}
