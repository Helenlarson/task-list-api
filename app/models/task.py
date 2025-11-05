from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    completed_at: Mapped[str | None] = mapped_column(nullable=True)
    
def to_dict(self):
    return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "is_completed": self.completed_at is not None,
    }

@classmethod
def from_dict(cls, data: dict) -> "Task":
    title = data["title"]
    description = data["description"]
    is_complete = data.get("is_complete", False)
    
    return cls(title=title, description=description, completed_at=completed_at)