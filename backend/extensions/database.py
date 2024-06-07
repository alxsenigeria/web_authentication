from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
  ...


db = SQLAlchemy(model_class=BaseModel)