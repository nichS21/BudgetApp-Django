import logging

import sys

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from application.routers import incomes, expenses, contributions, overview
from application.config import get_settings

# Application environment variables
settings = get_settings()

# Configure logger
log_format: str = '[%(asctime)s] (%(levelname)s) %(message)s'
log_date_format: str = '%m/%d/%Y %I:%M:%S %p'                           # Ex: 8/17/2026  11:46:36 AM
log_level: int = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(level=log_level, 
                    format=log_format, 
                    datefmt=log_date_format,
                    handlers=[
                        logging.StreamHandler(sys.stderr)               # Log to standard error output (console)
                    ],)             


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
