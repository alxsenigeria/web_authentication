from extensions.database import BaseModel
from sqlalchemy import Column, Integer, String

class User(BaseModel):

  __tablename__ = "users"

  id = Column(Integer, primary_key=True, autoincrement=True)
  first_name = Column(String(50))
  last_name = Column(String(50))
  email = Column(String(50), unique=True)
  password = Column(String(255))