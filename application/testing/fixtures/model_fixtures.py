import pytest_asyncio

from application.models import User

'''
Note: The modal fixtures here are not commited to the test database
    from here, because they would be deleted as soon as their respective 
    function finishes execution, since the tests are configured to each run 
    with a clean database that is then torn down.

In other words, these fixtures have to be added to the database explicitly
in the tests they are required in.
'''

@pytest_asyncio.fixture
async def user():
    return User(
        email="test@email.com",
        hashed_password="hashed"
    )
