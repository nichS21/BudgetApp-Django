from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .routers import income
from database import SessionDep

# Intialize Web API
app = FastAPI()

# Include the routers mapping to each part of the API
app.include_router(income.income_router)


@app.get("/")
def root():
        data = {"message": "Budget API is running."}
        return JSONResponse(content=data, status_code=200)
