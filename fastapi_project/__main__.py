import uvicorn

from .app import app

if __name__ == "__main__":
    """
    This is the main entry point of the FastAPI project.
    It runs the FastAPI application using uvicorn server.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)
