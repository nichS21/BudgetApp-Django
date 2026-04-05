from fastapi import FastAPI
from .routers import annual_and_tax

# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


app = FastAPI()

# Include the routers mapping to each part of the API
app.include_router(annual_and_tax.income_router)



@app.get("/")
async def root():
        return {"message": "Budget API is running."}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}