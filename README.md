# Task Manager API

A beginner-friendly REST API for managing tasks/todos, built with **FastAPI** and **SQLite**.

## About

This project demonstrates how to build a CRUD (Create, Read, Update, Delete) API using FastAPI with a raw SQLite database connection (no ORM). It includes:

- Task creation with title, description, priority, and category
- Task status tracking: `pending` -> `in_progress` -> `completed`
- Filtering tasks by status, priority, or category
- API documentation via Swagger UI, ReDoc, and Scalar

## Project Structure

```
test01/
├── app/
│   ├── __init__.py      # Package init
│   ├── schemas.py       # Pydantic models for request/response validation
│   ├── database.py      # SQLite database class with CRUD operations
│   └── routes.py        # API route definitions
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── README.md
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

#### Using Uvicorn

```bash
# Basic
uvicorn main:app

# With auto-reload (recommended for development)
uvicorn main:app --reload

# Custom host and port
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

#### Using FastAPI CLI

First install the FastAPI CLI:

```bash
pip install "fastapi[standard]"
```

Then run:

```bash
# Development mode (auto-reload enabled by default)
fastapi dev main.py

# Production mode
fastapi run main.py

# Custom host and port
fastapi dev main.py --host 0.0.0.0 --port 8080
```

## API Documentation

Once the app is running, visit these URLs in your browser:

| URL                          | Description                        |
| ---------------------------- | ---------------------------------- |
| http://localhost:8000        | Root endpoint (welcome message)    |
| http://localhost:8000/docs   | Swagger UI (interactive testing)   |
| http://localhost:8000/redoc  | ReDoc (alternative docs)           |
| http://localhost:8000/scalar | Scalar (modern API documentation)  |

## API Endpoints

| Method   | Endpoint        | Description                                          |
| -------- | --------------- | ---------------------------------------------------- |
| `GET`    | `/`             | Welcome message                                      |
| `POST`   | `/tasks/`       | Create a new task                                    |
| `GET`    | `/tasks/`       | List all tasks (filter by status, priority, category)|
| `GET`    | `/tasks/{id}`   | Get a single task by ID                              |
| `PUT`    | `/tasks/{id}`   | Update a task (partial updates supported)            |
| `DELETE` | `/tasks/{id}`   | Delete a task by ID                                  |

## Example Requests

### Create a task

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Complete the tutorial", "priority": "high", "category": "learning"}'
```

### Get all tasks

```bash
curl http://localhost:8000/tasks/
```

### Filter tasks by status

```bash
curl "http://localhost:8000/tasks/?status=pending"
```

### Update a task

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete a task

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Database

The app uses SQLite. A `tasks.db` file is automatically created in the project root when the app starts. You can view the database contents in VS Code using the **SQLite Viewer** extension.

## Tech Stack

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **SQLite** - Database
- **Pydantic** - Data validation
- **Scalar** - API documentation UI
