# app/models/goal.py
from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Dict, Any
from ..db import db

class Goal(db.Model):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[List["Task"]] = relationship(back_populates="goal", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "title": self.title}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Goal":
        return cls(title=data["title"])
