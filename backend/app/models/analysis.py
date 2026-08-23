"""
Analysis ORM model — stores each food freshness analysis result.
"""

import uuid
import json
from datetime import datetime, timezone

from sqlalchemy import String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Analysis(Base):
    """A single food freshness analysis record."""

    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    image_path: Mapped[str] = mapped_column(String(500), nullable=False)
    thumbnail_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    food_category: Mapped[str] = mapped_column(String(50), nullable=False)
    freshness_class: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    observations: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="analyses")

    @property
    def observations_list(self) -> list[str]:
        """Parse observations JSON string to list."""
        try:
            return json.loads(self.observations)
        except (json.JSONDecodeError, TypeError):
            return []

    @observations_list.setter
    def observations_list(self, value: list[str]):
        """Serialize list to JSON string."""
        self.observations = json.dumps(value)

    def __repr__(self) -> str:
        return f"<Analysis(id={self.id}, food={self.food_category}, freshness={self.freshness_class})>"
