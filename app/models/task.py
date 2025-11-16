# app/models/task.py
from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional, Dict, Any
from datetime import datetime
from ..db import db

class Task(db.Model):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"), nullable=True)
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self) -> Dict[str, Any]:
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        return cls(
            title=data["title"],
            description=data["description"],
            completed_at=None
        )
    

