import asyncio

import pytest

from httpx import AsyncClient

from fastapi import status

from sqlalchemy import ScalarResult, select

from application.models.income import Income
from application.models.user import User
from application.testing.fixtures.infrastructure_fixtures import test_api, session
from application.testing.fixtures.model_fixtures import user


@pytest.mark.asyncio
async def test_income_create_successful(user: User, test_api, session) -> None: 
    # Add user to DB and get its assigned ID
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user_id: int = user.id
    income_tax: float = 20.5
    annual_salary: int = 90000

    response = await test_api.post(
        "/income/",
        json={
            "annual_salary": annual_salary,
            "income_tax": income_tax,
            "user_id": user_id
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "Created annual income and tax successfully"}

    # Query DB to verify was created
    result: ScalarResult = await session.scalars(select(Income).where(Income.user_id == user_id))
    income: Income = result.one()

    assert income.annual_salary == annual_salary
    assert income.income_tax == income_tax
    assert income.user_id ==  user_id



@pytest.mark.asyncio
async def test_income_create_unsuccessful(test_api: AsyncClient, user: User, test_db) -> None:
    user_id: int = user.id
    income_tax: str = "bad data"
    annual_salary: str = "more bad data"

    response = await test_api.post(
        "/income/",
        json={
            "annual_salary": annual_salary,
            "income_tax": income_tax,
            "user_id": user_id
        }
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"message": "Failed to create an income and tax for this user."}

    # Query database to verify that was NOT created
    try:
        result: ScalarResult = await test_db.scalars(select(Income).where(Income.user_id == user_id))
        income: Income = result.one()
        # Note: it might make more sense to just do a count here lowkey
        # \
        # then figure out how to delete datafrom database after test is done
    except:
        pass





# test unsuccessful create - no user

# test unsuccessful (income already exists/user already has an income object)


# Continue with rest of testing and create all needed variations for the tests