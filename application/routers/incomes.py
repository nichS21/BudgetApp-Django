import json

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from sqlalchemy import ScalarResult, select, update

from application.database import SessionDep
from application.models.income import Income, IncomeCreate, IncomeSchema, IncomeUpdate


income_router = APIRouter(
    prefix="/income",
    tags=["Annual Salary and Income Tax"]
)


@income_router.post(
        "/",
        summary="Create annual salary, and income tax rate",
        description="Create an annual salary with estimated income tax for this user."
        )
async def create_income_and_tax(data: IncomeCreate, session: SessionDep) -> JSONResponse:
    try:
        user_income = Income(annual_salary=data.annual_salary, 
                             income_tax=data.income_tax,
                             user_id=data.user_id)
        session.add(user_income)
        await session.commit()
    except Exception as e:
        # TODO: add logging here to capture the exception
        content = {"message": "Failed to create an income and tax for this user."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    content = {"message": "Created annual income and tax successfully"}
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED) 


@income_router.get(
        "/{user_id}",
        summary="Retrive annual salary and income tax rate",
        description="Retrieve the annual salary and income tax rate for this user"
        )
async def get_income_and_tax(user_id: int, session: SessionDep):
    try:
        result: ScalarResult = await session.scalars(select(Income).where(Income.user_id == user_id))
        result = result.one()
        income_schema: IncomeSchema = IncomeSchema()
        income_json = income_schema.dump(result)
    except Exception as e:
        # TODO: add logging here to capture the exception
        content = {"message": "Failed retrieve annual income and tax for this user."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    content = {
        "message": "Successfully retrieved date for this user", 
        "income": income_json
        }
    
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@income_router.patch(
        "/{user_id}",
        summary="Update annual salary and income tax rate",
        description="Update the annual salary and income tax rate for this user."
        )
async def update_income_and_tax(user_id: int, data: IncomeUpdate, session: SessionDep) -> JSONResponse:
    try:
        result = await session.execute(
           update(Income) 
           .where(Income.user_id == user_id)
           .values(annual_salary=data.annual_salary,
                   income_tax=data.income_tax)
        )
        await session.commit()

        # Check number of rows matched by where clause. If it is 0, then there are no income rows that were updated by 
        #   this query. In SQL, this would be a normal query that runs but effects 0 rows. 
        if result.rowcount is not 1: # type: ignore
            raise Exception("No income rows were matched with this user ID by the where clause, so none were updated")
    except Exception as e:
        # TODO: add logging here to capture the exception
        content = {"message": "Failed to update income and tax for this user."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    content = {"message": "Successfully updated income for this user."}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)