from fastapi import APIRouter

income_router = APIRouter(
    prefix="/income",
    tags=["Annual Salary and Income Tax"]
)


@income_router.post(
        "/{user_id}",
        summary="Create annual salary, and income tax rate",
        description="Create an annual salary with estimated income tax for this user."
        )
async def create_income_and_tax(user_id: int):
    pass


@income_router.get(
        "/{user_id}",
        summary="Retrive annual salary and income tax rate",
        description="Retrieve the annual salary and income tax rate for this user"
        )
async def get_income_and_tax(user_id: int):
    pass


@income_router.patch(
        "/{user_id}",
        summary="Update annual salary and income tax rate",
        description="Update the annual salary and income tax rate for this user."
        )
async def update_income_and_tax(user_id: int):
    pass