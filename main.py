from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.routes import db, router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to database and create table
    db.connect_to_db()
    db.create_table()
    yield
    # Shutdown: close the database connection
    db.close()


app = FastAPI(
    title="Task Manager API",
    description="A beginner FastAPI project to manage tasks/todos with SQLite",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API. Visit /docs or /scalar for documentation."}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
