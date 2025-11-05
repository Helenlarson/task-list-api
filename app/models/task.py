from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Deixe title/description como opcionais (nullable=True) pois os testes constroem
    # objetos sem esses campos em alguns casos de to_dict.
    title: Mapped[Optional[str]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    # completed_at deve aceitar None e ser datetime
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def to_dict(self) -> dict:
        """Representação pública usada nas respostas JSON."""
        return {
            "id": self.id,  
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
 
        title = data["title"]          
        description = data["description"]
        is_complete = data.get("is_complete", False)

        completed_at = datetime.utcnow() if is_complete else None
        return cls(title=title, description=description, completed_at=completed_at)
