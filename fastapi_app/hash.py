from passlib.context import CryptContext
import pydantic

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash():
  def bcrypt(self, password: str):
    return pwd_cxt.hash(password)

  def verify(self, hashed_password: str, clean_password: str):
    return pwd_cxt.verify(clean_password, hashed_password)
