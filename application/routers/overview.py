import traceback

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from sqlalchemy import ScalarResult, select

from application.database import SessionDep
from application.models.income import Income, IncomeSchema
from application.models.expense import Expense, ExpenseSchema
from application.models.contribution import Contribution, ContributionSchema


overview_router = APIRouter(
    prefix="/overview",
    tags=["Overview of a user's income, expenses, and contributions "]
)


@overview_router.get(
    "/{user_id}",
    summary="Get overview for a user",
    description="Get income, expenses, and contributions with a break down per category, for a user"
)
async def get_overview(user_id: int, session: SessionDep) -> JSONResponse:
    # Get all data needed for this user's overview
    try:
        result: ScalarResult = await session.scalars(select(Income).where(Income.user_id == user_id))
        income = result.one()
        income_schema = IncomeSchema()
        income_json = income_schema.dump(income)

        result = await session.scalars(select(Contribution)
                                .add_columns((Contribution.amount * Contribution.frequency).label("monthly_cost"))
                                .where(Contribution.user_id == user_id))
        contributions = result.all()
        contributions_schema = ContributionSchema(many=True)
        contributions_json = contributions_schema.dump(contributions)

        contribution_monthly_total: int = 0
        for contribution in contributions:
            contribution_monthly_total += contribution.monthly_cost

        result = await session.scalars(select(Expense)
                                .add_columns((Expense.cost * Expense.frequency).label("monthly_cost"))
                                .where(Expense.user_id == user_id))
        expenses = result.all()
        expenses_schema = ExpenseSchema(many=True)
        expenses_json = expenses_schema.dump(expenses)

        expense_monthly_total = 0
        for expense in expenses:
            expense_monthly_total += expense.monthly_cost

    except Exception as e:
        # TODO: add specific error handling to each query so can track which one fails specifically - this can be handled by logger based on teh exception caught
        print(f"Exception:\n{e}")
        traceback.print_exc()

        content = {"message": "Failed to get user's overview."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
    content = {
        "message": "Succesfully retrieved contribution.",
        "income": income_json,
        "contributions": contributions_json,
        "contribution_monthly_total": str(contribution_monthly_total),
        "expenses": expenses_json,
        "expenses_monthly_total": str(expense_monthly_total)
    }

    return JSONResponse(content=content, status_code=status.HTTP_200_OK)