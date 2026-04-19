# Ensure can use SQLAlchemy models across multiple files and Alembic is able to discover all accordingly
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class ModelBase(AsyncAttrs, DeclarativeBase):
    pass

# Application model library
from .user import *
from .income import *

