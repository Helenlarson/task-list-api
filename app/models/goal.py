from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from ..db import db

class Goal(db.Model):
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[Optional[str]] = mapped_column(nullable=True)

    def to_dict(self):
        return {
            "id": self.id,         
            "title": self.title,   
        }

    @classmethod
    def from_dict(cls, data: dict):
        if "title" not in data:
            raise KeyError("title")
        return cls(title=data["title"])
