"""FastAPI app module."""

from fastapi import FastAPI

from fastapi_project.routers.opinions import router as opinions
from fastapi_project.routers.places import router as places

app = FastAPI()

app.include_router(places)
app.include_router(opinions)


@app.get("/", summary="Endpoint for health check.")
def health_check():
    """
    Summary: Endpoint for health check.

    Description: This endpoint is used to perform a health check of the application.
    It returns a dictionary with the status "ok".

    Returns:
        dict: A dictionary with the status "ok".
    """
    return {"status": "ok"}
