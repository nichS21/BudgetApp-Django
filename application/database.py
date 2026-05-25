from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from application.config import get_settings


settings = get_settings()

# Create underlying database engine (connection pool for whole app)
# NOTE: https://docs.sqlalchemy.org/en/21/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg
connection_str = settings.connection_str

if settings.debug is True:
    # Print out every database query to the console in development configuration
    engine = create_async_engine(connection_str, echo=True)
else: 
    engine = create_async_engine(connection_str, echo=False)


# Ensure that we use a single session, per request to the API
async def get_session():
    async with AsyncSession(engine) as session:
        yield session

# Create FastAPI dependency we can inject as needed, per endpoint
SessionDep = Annotated[AsyncSession, Depends(get_session)]