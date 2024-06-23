set shell := ["cmd.exe", "/c"]


create_tables:
    python -m fastapi_project.db.create_tables


run:
    uvicorn fastapi_project.app:app --reload --host 0.0.0.0 --port 8000

rund:
    docker-compose up --build

test:
    pytest --durations=10