from fastapi import APIRouter, HTTPException
from app.database import Database
from app.schemas import (
    TaskCreate,
    TaskResponse,
    TaskStatus,
    TaskPriority,
    TaskUpdate,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Database instance (will be initialized in main.py lifespan)
db = Database()


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """Create a new task."""
    result = db.create(task)
    return result


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    category: str | None = None,
):
    """Get all tasks. Optionally filter by status, priority, or category."""
    return db.get_all(
        status=status.value if status else None,
        priority=priority.value if priority else None,
        category=category,
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Get a single task by ID."""
    task = db.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    """Update a task. Only provided fields will be updated."""
    result = db.update(task_id, task)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Delete a task by ID."""
    deleted = db.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
