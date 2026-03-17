import sqlite3
from datetime import datetime
from typing import Any

from app.schemas import TaskCreate, TaskUpdate


class Database:
    def connect_to_db(self):
        """Connect to the SQLite database."""
        self.conn = sqlite3.connect("tasks.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        print("Connected to tasks.db ...")

    def create_table(self):
        """Create the tasks table if it doesn't exist."""
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                category TEXT,
                created_at TEXT
            )
        """)
        self.conn.commit()

    def create(self, task: TaskCreate) -> dict[str, Any]:
        """Insert a new task into the database."""
        created_at = datetime.now().isoformat()

        self.cur.execute(
            """
            INSERT INTO tasks (title, description, status, priority, category, created_at)
            VALUES (:title, :description, :status, :priority, :category, :created_at)
            """,
            {
                **task.model_dump(),
                "status": "pending",
                "created_at": created_at,
            },
        )
        self.conn.commit()

        new_id = self.cur.lastrowid
        return self.get(new_id)  # type: ignore

    def get(self, id: int) -> dict[str, Any] | None:
        """Get a single task by id."""
        self.cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))
        row = self.cur.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "category": row[5],
            "created_at": row[6],
        }

    def get_all(
        self,
        status: str | None = None,
        priority: str | None = None,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get all tasks with optional filters."""
        query = "SELECT * FROM tasks WHERE 1=1"
        params: list[str] = []

        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        if category:
            query += " AND category = ?"
            params.append(category)

        query += " ORDER BY id DESC"

        self.cur.execute(query, params)
        rows = self.cur.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
                "priority": row[4],
                "category": row[5],
                "created_at": row[6],
            }
            for row in rows
        ]

    def update(self, id: int, task: TaskUpdate) -> dict[str, Any] | None:
        """Update a task. Only updates fields that are provided (not None)."""
        existing = self.get(id)
        if existing is None:
            return None

        # Build dynamic update query with only provided fields
        update_data = task.model_dump(exclude_none=True)
        if not update_data:
            return existing

        set_clause = ", ".join(f"{key} = :{key}" for key in update_data)
        update_data["id"] = id

        self.cur.execute(
            f"UPDATE tasks SET {set_clause} WHERE id = :id",
            update_data,
        )
        self.conn.commit()

        return self.get(id)

    def delete(self, id: int) -> bool:
        """Delete a task by id. Returns True if a row was deleted."""
        existing = self.get(id)
        if existing is None:
            return False

        self.cur.execute("DELETE FROM tasks WHERE id = ?", (id,))
        self.conn.commit()
        return True

    def close(self):
        """Close the database connection."""
        print("...connection closed")
        self.conn.close()
