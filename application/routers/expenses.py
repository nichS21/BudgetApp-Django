import json

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from sqlalchemy import ScalarResult, delete, select, update

from application.database import SessionDep
from application.models.expense import Expense, ExpenseCreate, ExpenseSchema, ExpenseUpdate


expense_router = APIRouter(
    prefix="/expense",
    tags=["User's periodic expenses"]
)


@expense_router.post(
    "/",
    summary="Create an expense",
    description="Create an expense for a specified user"
)
async def create_expense(data: ExpenseCreate, session: SessionDep) -> JSONResponse:
    try: 
        expense = Expense(frequency=data.frequency, 
                          name=data.name,
                          description=data.description,
                          cost=data.cost,
                          user_id=data.user_id,
                          is_debt=data.user_id)
        session.add(expense)
        await session.commit()
    except:
        content = {"message": "Failed to create an expense for this user."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    content = {"message": "Created expense successfully."}
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@expense_router.get(
    "/{expense_id}",
    summary="Get an expense",
    description="Get an expense by its ID"
)
async def get_expense(expense_id: int, session: SessionDep) -> JSONResponse:
    try:
        result: ScalarResult = await session.scalars(select(Expense).where(Expense.id == expense_id))
        result = result.one()
        expense_schema: ExpenseSchema = ExpenseSchema()
        expense_json = expense_schema.dump(result)
    except:
        content = {"message": f"Failed to retrieve expense with ID: {expense_id}"}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    content = {
        "message": "Succesfully retrieved expense.",
        "expense": expense_json
    }

    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@expense_router.patch(
    "/{expense_id}",
    summary="Update an expense",
    description="Update an expense by its ID"
)
async def update_expense(expense_id: int, data: ExpenseUpdate, session: SessionDep) -> JSONResponse:
    try:
        await session.execute(
            update(Expense)
            .where(Expense.id == expense_id)
            .values(frequency=data.frequency,
                    name=data.name,
                    description=data.description,
                    cost=data.cost,
                    is_debt=data.is_debt)
        )
    except:
        content = {"message": "Failed to update expense."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    content = {"message": "Successfully updated expense."}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@expense_router.delete(
    "/{expense_id}",
    summary="Delete an expense",
    description="Delete an expense by its ID"
)
async def delete_expense(expense_id: int, session: SessionDep) -> JSONResponse:
    try:
        await session.execute(
            delete(Expense)
            .where(Expense.id == expense_id)
        )
    except:
        content = {"message": "Failed to delete given expense."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    content = {"message": "Succesfully deleted specified expense."}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@expense_router.get(
    "/expense-list/{user_id}",
    summary="List expenses by user",
    description="Get all the expenses tied to the specified user"
)
async def list_expenses(user_id: int, session: SessionDep) -> JSONResponse:
    try:
        result: ScalarResult = await session.scalars(select(Expense).where(Expense.user_id == user_id))
        results = result.all()
        expense_schema: ExpenseSchema = ExpenseSchema(many=True)
        expense_json = expense_schema.dump(results)
    except:
        content = {"message": "Failed to retrieve expenses for this user."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    content = {
        "message": "Succesfully retrieved expenses for this user.",
        "expenses": expense_json
    }

    return JSONResponse(content=content, status_code=status.HTTP_200_OK)
