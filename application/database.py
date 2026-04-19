from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


# Create underlying database engine (connection pool for whole app)
# NOTE: https://docs.sqlalchemy.org/en/21/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg
# TODO: Get connection details from environment varibles - no hardcoded values
# TODO 'echo=' should get from environment variables on whether or not is in development
connection_str = "postgresql+psycopg://postgres:postgres@localhost:5432/budget-api"
connect_args = {"check_same_thread": False}
engine = create_async_engine(connection_str, echo=True, connect_args=connect_args)


# Ensure that we use a single session, per request to the API
async def get_session():
    async with AsyncSession(engine) as session:
        yield session


# Create FastAPI dependency we can inject as needed, per endpoint
SessionDep = Annotated[AsyncSession, Depends(get_session)]
