import datetime
from typing import TYPE_CHECKING, List
import uuid
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from app.domain.entities.vehicle import Vehicle
# observar depois qual a melhor abordagem para o Base
from app.infrastructure.db.models.base import Base
from sqlalchemy.orm import relationship
if TYPE_CHECKING:
    from app.infrastructure.db.models.vehicle_model import VehicleModel

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now, nullable=False
    )
    last_updated: Mapped[datetime.datetime] = mapped_column(
        DateTime, onupdate=datetime.datetime.now, nullable=False
    )
    vehicles: Mapped[List["VehicleModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )