# Ensure can use SQLAlchemy models across multiple files and Alembic is able to discover all accordingly
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# Base to use for every model in the system, using needed mixins from SQLAlchemy
class ModelBase(AsyncAttrs, DeclarativeBase):
    pass

# Application model library
from .user import *
from .income import *
from .expense import *

