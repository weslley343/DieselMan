# app/infrastructure/db/models/scene_model.py

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import uuid4
from app.infrastructure.db.database import Base
import uuid

class SceneModel(Base):
    __tablename__ = "scenes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

    # backref automático, se quiser acessar user.scene_set ou similar
    user = relationship("UserModel", back_populates="scenes")
