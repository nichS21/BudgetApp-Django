import pytest

from application.models import User, Income

'''
Note: The modal fixtures here are not commited to the test database
    from here, because they would be deleted as soon as their respective 
    function finishes execution, since the tests are configured to each run 
    with a clean database that is then torn down.

In other words, these fixtures have to be added to the database explicitly
in the tests they are required in.
'''

@pytest.fixture
def user() -> User:
    return User(
        email="test@email.com",
        hashed_password="hashed"
    )


@pytest.fixture
def income() -> Income:
    return Income(
        annual_salary=90000,
        income_tax=22.0
    )