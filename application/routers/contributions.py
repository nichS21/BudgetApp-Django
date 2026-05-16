import json

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from sqlalchemy import ScalarResult, delete, select, update

from application.database import SessionDep
from application.models.contribution import Contribution, ContributionCreate, ContributionUpdate, ContributionSchema


contribution_router = APIRouter(
    prefix="/contribution",
    tags=["User's periodic contributions"]
)


@contribution_router.post(
    "/",
    summary="Create a contribution",
    description="Create a contribution for a specified user"
)
async def create_contribution(data: ContributionCreate, session: SessionDep) -> JSONResponse:
    try:
        contribution = Contribution(frequency=data.frequency,
                                    name=data.name,
                                    description=data.description,
                                    amount=data.amount,
                                    user_id=data.user_id,
                                    type=data.type
                                    )
        session.add(contribution)
        await session.commit()
    except:
        content = {"message": "Failed to create a contribution for this user."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    content= {"message": "Create contribution successfully"}
    return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)


@contribution_router.get(
    "/{contribution_id}",
    summary="Get a contribution",
    description="Get a contribution by its ID"
)
async def get_contribution(contribution_id: int, session: SessionDep) -> JSONResponse:
    try:
        result: ScalarResult = await session.scalars(select(Contribution).where(Contribution.id == contribution_id))
        result = result.one()
        contribution_schema: ContributionSchema = ContributionSchema()
        contribution_json = contribution_schema.dump(result)
    except:
        content = {"message": f"Failed to retrieve contribution with ID: {contribution_id}"}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    content = {
        "message": "Succesfully retrieved contribution.",
        "contribution": contribution_json
    }

    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@contribution_router.patch(
    "/{contribution_id}",
    summary="Update a contribution",
    description="Update a contribution by its ID"
)
async def update_contribution(contribution_id: int, data: ContributionUpdate, session: SessionDep) -> JSONResponse:
    try:
        await session.execute(
            update(Contribution)
            .where(Contribution.id == contribution_id)
            .values(frequency=data.frequency,
                    name=data.name,
                    description=data.description,
                    amount=data.amount,
                    type=data.amount)
        )
    except:
        content = {"message": "Failed to update contribution."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    content = {"message": "Successfully updated contribution."}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@contribution_router.delete(
    "/{contribution_id}",
    summary="Delete a contribution",
    description="Delete a contribution by its ID"
)
async def delete_contribution(contribution_id: int, session: SessionDep) -> JSONResponse:
    try:
        await session.execute(
            delete(Contribution)
            .where(Contribution.id == contribution_id)
        )
    except:
        content = {"message": "Failed to delete given contribution."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    content = {"message": "Succesfully deleted specified contribution."}
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@contribution_router.get(
    "/contribution-list/{user_id}",
    summary="List all contributions by user",
    description="Get all contributions tied to the specified user"
)
async def list_contributions(user_id: int, session: SessionDep) -> JSONResponse:
    try:
        result: ScalarResult = await session.scalars(select(Contribution).where(Contribution.user_id == user_id))
        results = result.all()
        contribution_schema: ContributionSchema = ContributionSchema(many=True)
        contribution_json = contribution_schema.dump(results)
    except:
        content = {"message": "Failed to retrieve contributions for this user."}
        return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    content = {
        "message": "Succesfully retrieved contributions for this user.",
        "contributions": contribution_json
    }

    return JSONResponse(content=content, status_code=status.HTTP_200_OK)
