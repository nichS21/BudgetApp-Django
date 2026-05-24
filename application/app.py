from fastapi import FastAPI
from fastapi.responses import JSONResponse

from application.routers import incomes, expenses, contributions, overview

# Intialize Web API
app = FastAPI()

# Include the routers mapping to each part of the API
app.include_router(incomes.income_router)
app.include_router(expenses.expense_router)
app.include_router(contributions.contribution_router)
app.include_router(overview.overview_router)


@app.get("/")
def root():
        data = {"message": "Budget API is running."}
        return JSONResponse(content=data, status_code=200)
