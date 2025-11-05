from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class RefreshToken(Base):
    """
    Modelo para almacenar refresh tokens en la base de datos.
    Permite invalidar tokens específicos y gestionar sesiones de usuario.
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    user = relationship("User", back_populates="refresh_tokens")

    def is_valid(self) -> bool:
        """
        Verifica si el refresh token es válido
        (no revocado y no expirado)
        """
        return not self.is_revoked and self.expires_at > datetime.utcnow()
